from functools import lru_cache
import os
from pathlib import Path
from typing_extensions import Literal
from pydantic import BaseModel, Field, SecretStr, field_validator
from dotenv import load_dotenv
from pathlib import Path


PROJECT_ROOT = Path(__file__).resolve().parents[3]

ENV_FILE = PROJECT_ROOT / ".env"

LogLevel = Literal["DEBUG", "INFO", "WARNING", "ERROR", "CRITICAL"]

DEFAULT_GEMINI_MODEL = "gemini-3.8-flash"
class Settings(BaseModel):
   model: str = DEFAULT_GEMINI_MODEL
   gemini_api_key: SecretStr
   gemini_temprature : float = Field(default=0.0, gt= 0.0, le=1.0, description="Temperature for the Gemini model (between 0 and 1).")
   log_level: LogLevel = "INFO"
   
   @field_validator("gemini_api_key")
   @classmethod
   def validate_gemini_api_key(cls,value):
       key = value.get_secret_value().strip()
       if not key:
           raise ValueError("GOOGLE_API_KEY is not set in the environment variables.")
       return SecretStr(key)
   
   @classmethod
   def load_from_env(cls):
       return cls.model_validate(
           {
               "model": os.getenv("MODEL", DEFAULT_GEMINI_MODEL),
               "gemini_api_key": SecretStr(os.getenv("GOOGLE_API_KEY", "")),
               "gemini_temprature": float(os.getenv("GEMINI_TEMPERATURE", 0.7)),
               "log_level": os.getenv("LOG_LEVEL", "INFO").upper(),
           }
       )

@lru_cache(maxsize=1)
def get_settings()->Settings:
    
    load_dotenv(dotenv_path=ENV_FILE,override=False)
    return Settings.load_from_env()