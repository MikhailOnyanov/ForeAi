from ..services.base_vector_db_service import BaseVectorDBService
from ..services.chroma_service import ChromaService


class VectorDBProvider:
    """Фабрика для выбора нужной векторной базы данных."""

    @staticmethod
    def get_vector_db_service(db_type: str, client_info: dict) -> BaseVectorDBService:
        """Возвращает объект сервиса в зависимости от типа базы данных."""
        if db_type == 'chroma':
            return ChromaService(client_info)
        raise NotImplementedError(f"База данных '{db_type}' не поддерживается.")
