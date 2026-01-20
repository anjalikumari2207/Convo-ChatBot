from sqlalchemy import Column, Integer, String, Text
from database import Base

class UserMemory(Base):
    __tablename__ = "user_memory"

    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(String, unique=True, index=True)

    # Smart memory fields
    name = Column(String, nullable=True)
    interests = Column(Text, nullable=True)
    mood = Column(String, nullable=True)
    tone = Column(String, nullable=True)


    # Full conversation history
    conversation = Column(Text, default="")
