import os

# Maximum length of a message
MAX_SYM = 4095

# Get Telegram bot key from .env file
TELEGRAM_API_KEY = os.getenv("TELEGRAM_API_KEY")

# URL to ForeAI API service
FORE_AI_BACKEND_API = os.getenv("FORE_AI_BACKEND_API")