import os
import json
from typing import Type, TypeVar, Optional, Any
from pydantic import BaseModel
from google import genai
from google.genai import types
from tenacity import retry, stop_after_attempt, wait_exponential
from src.utils.logging_utils import log
import yaml

# Generic type for Pydantic models
T = TypeVar("T", bound=BaseModel)

class LLMClient:
    """
    Wrapper for Google GenAI SDK (V2) with retry logic and structured output support.
    """
    def __init__(self, config_path: str = "config/config.yaml"):
        self.api_key = os.getenv("GOOGLE_API_KEY")
        if not self.api_key:
            log.warning("GOOGLE_API_KEY not found in environment variables. LLM calls will fail.")
        
        try:
            with open(config_path, "r") as f:
                self.config = yaml.safe_load(f)
        except FileNotFoundError:
            log.error(f"Config file not found at {config_path}")
            raise
            
        self.client = genai.Client(api_key=self.api_key)
        self.model_name = self.config.get("llm", {}).get("model_name", "gemini-1.5-flash")
        self.temperature = self.config.get("llm", {}).get("temperature", 0.0)

    @retry(stop=stop_after_attempt(3), wait=wait_exponential(multiplier=1, min=2, max=10))
    def generate_structured(
        self, 
        prompt: str, 
        response_schema: Type[T],
        system_instruction: Optional[str] = None
    ) -> T:
        """
        Generate a structured response matching a Pydantic model.
        """
        try:
            log.debug(f"Generating structured output with model: {self.model_name}")
            
            response = self.client.models.generate_content(
                model=self.model_name,
                contents=prompt,
                config=types.GenerateContentConfig(
                    system_instruction=system_instruction,
                    temperature=self.temperature,
                    response_mime_type="application/json",
                    response_schema=response_schema
                )
            )
            
            if not response.parsed:
                raise ValueError("LLM returned empty parsed response")
                
            return response.parsed
            
        except Exception as e:
            log.error(f"Structured generation failed: {str(e)}")
            raise

    @retry(stop=stop_after_attempt(3), wait=wait_exponential(multiplier=1, min=2, max=10))
    def generate_text(
        self, 
        prompt: str, 
        system_instruction: Optional[str] = None
    ) -> str:
        """
        Generate free-form text response.
        """
        try:
            log.debug(f"Generating text output with model: {self.model_name}")
            
            response = self.client.models.generate_content(
                model=self.model_name,
                contents=prompt,
                config=types.GenerateContentConfig(
                    system_instruction=system_instruction,
                    temperature=self.temperature
                )
            )
            
            if not response.text:
                return ""
            
            return response.text
            
        except Exception as e:
            log.error(f"Text generation failed: {str(e)}")
            raise
