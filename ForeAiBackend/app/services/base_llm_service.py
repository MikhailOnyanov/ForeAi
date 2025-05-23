from abc import ABC, abstractmethod
from typing import Any


class BaseLLMService(ABC):
    """Базовый класс для всех сервисов LLM."""

    @abstractmethod
    def query(self, input_message: str, knowledge_text_corpus) -> Any:
        """Оотправить текст на генерацию ответа."""
        raise NotImplementedError
