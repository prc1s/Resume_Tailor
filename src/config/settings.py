"""
Configuration settings for CVTailor application.
"""
import os
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

class Settings:
    """Application settings and configuration."""
    
    # OpenAI Configuration
    OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")
    OPENAI_MODEL = "gpt-3.5-turbo"
    OPENAI_TEMPERATURE = 0.7
    OPENAI_MAX_TOKENS = 2500
    
    # Application Configuration
    APP_NAME = "CVTailor"
    APP_VERSION = "1.1.0"
    APP_DESCRIPTION = "Generate Your Professional CV in 60 Seconds"
    
    # File Paths
    PROMPTS_FILE = "data/prompts.json"
    LOGS_FILE = "data/logs.db"
    DATABASE_FILE = "data/cv_data.db"
    
    # Pricing Configuration
    FREE_TRIAL_LIMIT = 1
    PAID_PRICE_SAR = 29
    PRICE_PER_CV = 29
    SUBSCRIPTION_PRICE_SAR = 59
    
    # Application Version
    VERSION = "1.1.0"
    
    # Supported Languages and Tones
    SUPPORTED_LANGUAGES = ["en", "ar"]
    SUPPORTED_TONES = ["formal", "friendly"]
    
    # Form Configuration
    REQUIRED_FIELDS = ["job_description", "education"]
    
    # Validation
    MIN_JOB_DESCRIPTION_LENGTH = 10
    MIN_EDUCATION_LENGTH = 5

    # Admin Configuration
    ADMIN_SECRET_KEY = os.getenv("ADMIN_SECRET_KEY")

    # Email Configuration
    EMAIL_HOST = os.getenv("EMAIL_HOST")
    EMAIL_PORT = int(os.getenv("EMAIL_PORT", 587))
    EMAIL_HOST_USER = os.getenv("EMAIL_HOST_USER")
    EMAIL_HOST_PASSWORD = os.getenv("EMAIL_HOST_PASSWORD")
    EMAIL_SENDER_NAME = os.getenv("EMAIL_SENDER_NAME", "CVTailor")

# Global settings instance
settings = Settings() 