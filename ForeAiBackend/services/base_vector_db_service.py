from abc import ABC
from typing import Optional, Collection, List


class BaseVectorDBService(ABC):
    """Базовый класс для всех сервисов векторных БД."""

    def get_collection(self, collection_name: str) -> Optional[Collection]:
        """Получает коллекцию по имени."""
        raise NotImplementedError

    def get_collection_info(self, collection_name: str) -> Optional[dict]:
        """Получает информацию о коллекции."""
        raise NotImplementedError

    def query_collection(self, collection_name: str, query_params: dict) -> dict:
        """Выполняет запрос к коллекции."""
        raise NotImplementedError

    def add_to_collection(self, docs: List[dict], collection_name: str):
        """Добавляет документы в коллекцию."""
        raise NotImplementedError
