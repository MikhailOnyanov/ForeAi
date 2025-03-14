from dotenv import dotenv_values

# Maximum length of a message
MAX_SYM = 4095

# Get Telegram bot key from .env file
TELEGRAM_API_KEY = dotenv_values(".env").get("TELEGRAM_API_KEY")

# URL to ForeAI API service
FORE_AI_BACKEND_API = "http://127.0.0.1:8000/docs/get_vector"
