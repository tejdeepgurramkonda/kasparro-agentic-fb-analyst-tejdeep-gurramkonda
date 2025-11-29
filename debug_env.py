import os
from dotenv import load_dotenv

print(f"CWD: {os.getcwd()}")
loaded = load_dotenv(dotenv_path=".env", verbose=True)
print(f"Loaded .env: {loaded}")

key = os.getenv("GOOGLE_API_KEY")
if key:
    print(f"✅ GOOGLE_API_KEY found: {key[:4]}...{key[-4:]}")
else:
    print("❌ GOOGLE_API_KEY not found in environment.")
