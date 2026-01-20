from fastapi import FastAPI, Request, Response
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
from fastapi.responses import FileResponse
from pydantic import BaseModel
import google.generativeai as genai
import os
from dotenv import load_dotenv
from sqlalchemy.orm import Session

from database import engine, SessionLocal
from models import UserMemory, Base
from memory_extractor import extract_user_memory
from tone_detector import detect_tone
from identity_guard import handle_identity_and_trick_questions

# ---------------- ENV SETUP ----------------

load_dotenv()
genai.configure(api_key="AIzaSyC6DnuEkm0G6fINVmpoUMf7Rn0Ab6OAXFA")
print("API KEY FOUND:", bool(os.getenv("GEMINI_API_KEY")))

genai.configure(api_key=os.getenv("GEMINI_API_KEY"))

# ---------------- APP INIT ----------------

app = FastAPI(
    title="STAN Conversational Chatbot",
    version="1.0.0"
)

# CORS (VERY IMPORTANT)
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

Base.metadata.create_all(bind=engine)

# Serve frontend static files and index
app.mount("/static", StaticFiles(directory="frontend"), name="static")


@app.get("/")
def serve_frontend():
    return FileResponse("frontend/index.html")


# Handle CORS preflight for /chat explicitly (middleware should handle it,
# but this ensures an explicit 200 for OPTIONS requests)
@app.options("/chat")
def chat_options():
    return Response(status_code=200)

# ---------------- REQUEST MODEL ----------------

class ChatRequest(BaseModel):
    user_id: str
    message: str

# ---------------- HELPERS ----------------

def get_db():
    db = SessionLocal()
    try:
        return db
    finally:
        db.close()

def get_or_create_user(db: Session, user_id: str):
    user = db.query(UserMemory).filter(UserMemory.user_id == user_id).first()
    if not user:
        user = UserMemory(user_id=user_id, conversation="")
        db.add(user)
        db.commit()
        db.refresh(user)
    return user

def generate_ai_reply(context: str, message: str):
    model = genai.GenerativeModel("gemini-3-flash")
    prompt = f"""
You are a human-like assistant.
Never say you are an AI or bot.

Context:
{context}

User says:
{message}

Reply naturally.
"""
    return model.generate_content(prompt).text

# ---------------- CHAT ENDPOINT ----------------

@app.post("/chat")
def chat(request: ChatRequest):
    user_id = request.user_id
    message = request.message

    db = get_db()
    user = get_or_create_user(db, user_id)

    guard = handle_identity_and_trick_questions(message)
    if guard:
        return {"reply": guard}

    extracted = extract_user_memory(message)
    if "name" in extracted:
        user.name = extracted["name"]
    if "interests" in extracted:
        user.interests = extracted["interests"]
    if "mood" in extracted:
        user.mood = extracted["mood"]

    user.tone = detect_tone(message)
    user.conversation += f"\nUser: {message}"

    context = f"""
Name: {user.name}
Interests: {user.interests}
Mood: {user.mood}
Tone: {user.tone}
Conversation:
{user.conversation}
"""

    # If GEMINI API key is not configured, return a fast fallback reply
    if not os.getenv("GEMINI_API_KEY"):
        reply = "Sorry, AI service is not configured on the server."
    else:
        try:
            reply = generate_ai_reply(context, message)
        except Exception as e:
            # Fallback reply when AI service fails or is unreachable
            print("AI generation error:", e)
            reply = "Sorry, I'm having trouble connecting to the AI service right now."

    user.conversation += f"\nBot: {reply}"

    db.commit()

    return {"reply": reply}
