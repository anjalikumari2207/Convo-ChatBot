import google.generativeai as genai

genai.configure(api_key="AIzaSyC6DnuEkm0G6fINVmpoUMf7Rn0Ab6OAXFA")

model = genai.GenerativeModel("gemini-3-flash")
response = model.generate_content("Say hello in one sentence")
print(response.text)
