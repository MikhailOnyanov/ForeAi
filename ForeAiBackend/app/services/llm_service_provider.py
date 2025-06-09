from ..services.base_llm_service import BaseLLMService
from ..services.yandex_gpt_service import YandexGptService


class LLMServiceProvider:
    """Фабрика для выбора нужной LLM."""

    @staticmethod
    def get_llm_service(llm_title: str) -> BaseLLMService:
        """Возвращает объект сервиса в зависимости от типа базы данных."""
        if llm_title == 'YandexGPT':
            return YandexGptService()
        raise NotImplementedError(f"LLM '{llm_title}' не поддерживается.")
