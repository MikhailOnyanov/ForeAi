from ..internal.foresight_docs_logic import parse_chromadb_query_to_foresight_documents_old
from ..services.llm_service_provider import LLMServiceProvider
from ..services.vector_db_provider import VectorDBProvider
from ..dependencies import get_chroma_client
import logging

logger = logging.getLogger(__name__)

class MessageService:
    def __init__(self):
        # Параметры для запроса к векторной БД
        self.base_query_params = {'n_results': '3'}
        pass

    def make_response(self, message):
        db_service = get_chroma_client()
        llm_service = LLMServiceProvider.get_llm_service("YandexGPT")
        logger.info("Got YandexGPT service")

        logger.info("Querying fore_collection from CHROMA")
        query_params = {'n_results': 3, 'query_texts': [message]}
        # Поиск документации для поставки в модель
        responses_from_db_service = db_service.query_collection('fore_collection', query_params)
        logger.info(f"Successfully queried CHROMA with response of: {len(responses_from_db_service)}")
        # Нормализация ответов.
        normalized_responses = parse_chromadb_query_to_foresight_documents_old(responses_from_db_service)

        # Отправка исходного сообщения и дополнительных знаний в модель
        logger.info(f"Querying GPT with message: {message}")
        response_from_llm_service: str = llm_service.query(message, normalized_responses)


        return response_from_llm_service
