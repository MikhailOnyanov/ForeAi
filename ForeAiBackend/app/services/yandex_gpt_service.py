from typing import Any
import datetime
from ..services.base_llm_service import BaseLLMService


class YandexGptService(BaseLLMService):
    def __init__(self):
        BaseLLMService.__init__(self)

    def query(self, input_message: str, knowledge_text_corpus: dict[Any]) -> Any:
        """Оотправить текст на генерацию ответа."""
        # TODO: логику обработки
        response_from_llm = self.response_generation_pipeline(input_message, knowledge_text_corpus)
        return response_from_llm

    def response_generation_pipeline(self, input_message: str, knowledge_text_corpus: Any) -> str:
        """

        :param input_message:
        :type input_message:
        :param knowledge_text_corpus:
        :type knowledge_text_corpus: TODO пока не понятно, какой тип данных на вход
        :return:
        :rtype:
        """
        # Some magic with strings and preprompt ...
        pre_prompt_text = f"Help developer to solve task: {input_message}, here some docs: {[str(doc) for doc in knowledge_text_corpus]}"
        # ... API CALL ...
        # TODO: Для тестов сделан 1 элемент
        # api_response = self.send_to_api(pre_prompt_text)
        api_response = {"Data": f"{knowledge_text_corpus[0]}"}
        # ... UNPACKING RESPONSE TEXT FROM JSON...
        llm_text_response = self.unpack_api_response(api_response)
        # ... PREPARE MESSAGE FOR END-USER
        text_for_end_user = self.prepare_message_for_end_user(input_message, llm_text_response)
        return text_for_end_user

    def send_to_api(self, prepared_text: str) -> dict[str, Any]:
        return {
            "Status": 200,
            "Data": prepared_text,
            "Meta": f"{datetime.datetime.now().isoformat()}"
        }

    def unpack_api_response(self, api_response: dict) -> str:
        return api_response["Data"]

    def prepare_message_for_end_user(self, input_message: str, llm_response: str) -> str:
        return f"Конечно, я могу помочь Вам с вопросом по {input_message}, попробуйте начать с этого:\n{llm_response}"
