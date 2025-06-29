from abc import ABC, abstractmethod
from collections.abc import Collection


class BaseVectorDBService(ABC):
    """Базовый класс для всех сервисов векторных БД."""

    @abstractmethod
    def get_collection(self, collection_name: str) -> Collection | None:
        """Получает коллекцию по имени."""
        raise NotImplementedError

    @abstractmethod
    def get_collection_info(self, collection_name: str) -> dict | None:
        """Получает информацию о коллекции."""
        raise NotImplementedError

    @abstractmethod
    def query_collection(self, collection_name: str, query_params: dict) -> dict:
        """Выполняет запрос к коллекции."""
        raise NotImplementedError

    @abstractmethod
    def create_collection(self, collection_name: str) -> bool:
        """Создаёт коллекцию."""
        raise NotImplementedError

    @abstractmethod
    def add_to_collection(self, docs: list[dict], collection_name: str):
        """Добавляет документы в коллекцию."""
        raise NotImplementedError

    @abstractmethod
    def list_collections(self) -> list:
        """Возвращает список коллекций."""
        raise NotImplementedError
