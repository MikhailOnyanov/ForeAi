import hashlib
import json
from typing import Any


class HashingService:
    def __init__(self):
        pass
    @staticmethod
    def dict_hash(dictionary: dict[str, Any]) -> str:
        """Вычисляет MD5-хэш словаря.

        :param dictionary: Словарь для хэширования.
        :return: Строка с MD5-хэшем.
        """
        dhash = hashlib.md5()
        encoded = json.dumps(dictionary, sort_keys=True).encode()
        dhash.update(encoded)
        return dhash.hexdigest()
