from abc import ABC
from typing import Any


class BaseLLMService(ABC):
    """Базовый класс для всех сервисов LLM."""

    def query(self, input_message: str, knowledge_text_corpus) -> Any:
        """Оотправить текст на генерацию ответа."""
        raise NotImplementedError
    # TODO: методы подключения
