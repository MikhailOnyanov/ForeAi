import logging

# Настройка логирования
logging.basicConfig(
    format="%(asctime)s - [%(levelname)s] - %(name)s - %(message)s",
    level=logging.INFO,
    handlers=[
        logging.FileHandler("app.log"),  # Запись логов в файл
        logging.StreamHandler()  # Вывод в консоль
    ]
)

logger = logging.getLogger("ForeAiBackend")