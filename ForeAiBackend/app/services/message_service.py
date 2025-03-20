from ..internal.foresight_docs_logic import parse_chromadb_query_to_foresight_documents_old
from ..services.llm_service_provider import LLMServiceProvider
from ..services.vector_db_provider import VectorDBProvider
from ..constants import client_info


class MessageService:
    def __init__(self):
        self.base_query_params = {'n_results': '3'}
        pass

    def make_response(self, message):
        db_service = VectorDBProvider.get_vector_db_service("chroma", client_info)
        llm_service = LLMServiceProvider.get_llm_service("YandexGPT")

        query_params = {'n_results': 3, 'query_texts': [message]}

        responses_from_db_service = db_service.query_collection('fore_collection', query_params)

        normalized_responses = parse_chromadb_query_to_foresight_documents_old(responses_from_db_service)

        # Пока что возвращает корпуса текстов из векторной БД
        response_from_llm_service = llm_service.query(message, normalized_responses)


        return response_from_llm_service
