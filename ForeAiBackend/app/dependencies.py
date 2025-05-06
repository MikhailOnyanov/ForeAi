import logging
from typing import Annotated

from fastapi import Depends

from app.common import get_chroma_creds
from app.services.base_vector_db_service import BaseVectorDBService
from app.services.vector_db_provider import VectorDBProvider

logger = logging.getLogger(__name__)

def initialize_vector_db(db_type_name: str, creds: dict) -> BaseVectorDBService:
    vector_db = VectorDBProvider.get_vector_db_service(db_type_name, creds)
    return vector_db


#ChromaClientCredsDep = Annotated[dict, Depends(get_chroma_creds)]
