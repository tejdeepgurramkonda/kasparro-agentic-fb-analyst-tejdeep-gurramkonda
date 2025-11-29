import os
from dotenv import load_dotenv
from google import genai

load_dotenv()

client = genai.Client(api_key=os.getenv("GOOGLE_API_KEY"))

print("Listing FLASH models...")
try:
    for m in client.models.list():
        if "flash" in m.name:
            print(f"Model: {m.name}")
except Exception as e:
    print(f"Error listing models: {e}")
