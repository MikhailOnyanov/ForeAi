import logging
from functools import cache
from typing import Annotated

from fastapi import Depends

from app.conifg import ChromaConfig
from app.services.base_vector_db_service import BaseVectorDBService
from app.services.chroma_service import ChromaService
from app.services.vector_db_provider import VectorDBProvider


logger = logging.getLogger(__name__)

def initialize_vector_db(db_type_name: str, creds: dict) -> BaseVectorDBService:
    """Инициализирует векторную базу данных заданного типа."""
    vector_db = VectorDBProvider.get_vector_db_service(db_type_name, creds)
    return vector_db

@cache
def get_chroma_client() -> ChromaService:
    return ChromaService(ChromaConfig())

ChromaServiceDep = Annotated[ChromaService, Depends(get_chroma_client)]
