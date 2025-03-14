from typing import Any

from ..services.base_llm_service import BaseLLMService


class YandexGptService(BaseLLMService):
    def __init__(self):
        BaseLLMService.__init__(self)

    def query(self, input_message: str, knowledge_text_corpus: dict[Any]) -> Any:
        """Оотправить текст на генерацию ответа."""
        # TODO: логику обработки
        return knowledge_text_corpus
