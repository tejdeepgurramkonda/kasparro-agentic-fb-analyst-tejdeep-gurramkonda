import os
import sys
from src.utils.logging_utils import setup_logging, log
from src.utils.llm_client import LLMClient
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

def verify_foundation():
    # 1. Test Logging
    setup_logging(level="DEBUG")
    log.info("✅ Logging initialized successfully.")
    log.debug("This is a debug message.")

    # 2. Test LLM Client
    api_key = os.getenv("GOOGLE_API_KEY")
    if not api_key:
        log.warning("⚠️ GOOGLE_API_KEY not found. Skipping LLM test.")
        return

    try:
        client = LLMClient()
        log.info(f"✅ LLM Client initialized with model: {client.model_name}")
        
        response = client.generate_text("Say 'Hello, World!'")
        log.info(f"🤖 LLM Response: {response}")
        
        if "Hello" in response:
            log.info("✅ LLM connectivity verified.")
        else:
            log.error("❌ LLM response did not match expected output.")
            
    except Exception as e:
        log.error(f"❌ LLM verification failed: {e}")

if __name__ == "__main__":
    verify_foundation()
