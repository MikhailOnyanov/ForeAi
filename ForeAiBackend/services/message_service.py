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

        full_params = {'n_results': '3', 'query_texts': [message]}

        responses_from_db_service = db_service.query_collection(**full_params)
        # Пока что возвращает корпуса текстов из векторной БД
        response_from_llm_service = llm_service.query(message, responses_from_db_service)

        return response_from_llm_service
