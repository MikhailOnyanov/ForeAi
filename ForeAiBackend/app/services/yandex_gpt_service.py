import json
from typing import Any
import requests

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
        text_with_preprompt = f"Помоги решить вопрос пользователя: {input_message}, вот документация которая может пригодиться: {[str(doc) for doc in knowledge_text_corpus]}"
        # ... API CALL ...
        api_response = self.send_to_api(text_with_preprompt)
        # ... UNPACKING RESPONSE TEXT FROM JSON...
        llm_text_response = self.unpack_api_response(api_response)
        return llm_text_response

    def send_to_api(self, user_query_text: str) -> dict[str, Any]:
        """
        Отправляет запрос в YandexGPT
        :param user_query_text: Текст запроса к системе
        :return:
        :rtype:
        """
        prompt = {
            "modelUri": "gpt://b1g7mr6mvg5ennk001ja/yandexgpt-lite",
            "completionOptions": {
                "stream": False,
                "temperature": 0.6,
                "maxTokens": "2000"
            },
            "messages": [
                {
                    "role": "system",
                    "text": "Ты ассистент по разработке на языке программирования Fore, способный помочь разработчику платформы Форсайт и разработчику Fore сделать его работу."
                },
                {
                    "role": "user",
                    "text": f"{user_query_text}"
                }
            ]
        }

        url = "https://llm.api.cloud.yandex.net/foundationModels/v1/completion"
        headers = {
            "Content-Type": "application/json",
            "Authorization": "Api-Key X"
        }

        response = requests.post(url, headers=headers, json=prompt)

        return {
            "Status": 200,
            "Data": json.loads(response.text),
            "Meta": f"{datetime.datetime.now().isoformat()}"
        }

    def unpack_api_response(self, api_response: dict) -> str:
        data_to_unpack = api_response["Data"]["result"]["alternatives"][0]
        response_message_text = data_to_unpack["message"]["text"]

        return response_message_text
