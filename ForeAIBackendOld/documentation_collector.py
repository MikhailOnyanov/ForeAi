import time
import requests

from .parsers import text_from_html, find_header, find_version


# Метод собирает документацию по заданному массиву ссылок
def collect_docs(sites: list) -> list[dict]:
    results = []
    for url in sites:
        result = {}
        try:
            response = requests.get(url)

            result["Раздел документации"] = find_header(response.text)
            result["Текст раздела"] = text_from_html(response.text)
            result["Версия платформы"] = find_version(result["Текст раздела"])

        except Exception as ex:
            print(ex)

        results.append(result)

    return results
