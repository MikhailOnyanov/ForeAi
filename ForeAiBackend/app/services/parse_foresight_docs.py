import regex
import unicodedata
import requests
from bs4 import BeautifulSoup, Comment
from typing import Dict, List
import logging

logger = logging.getLogger(__name__)


def get_simple_texts(bs_instance: BeautifulSoup) -> List[str]:
    """
    Извлекает простой текст из параграфов, не содержащих атрибутов.

    :param bs_instance: Экземпляр BeautifulSoup с HTML-контентом.
    :return: Список текстов из простых параграфов.
    """
    return [p.get_text() for p in bs_instance.find_all('p') if not p.attrs]


def parse_code_blocks(bs_instance: BeautifulSoup) -> List[List[str]]:
    """
    Извлекает блоки кода из HTML-страницы.

    :param bs_instance: Экземпляр BeautifulSoup с HTML-контентом.
    :return: Список списков строк кода.
    """
    paragraphs_code = bs_instance.find_all('p', attrs={'style': "font-family: 'Courier New'; font-size: 10pt;"})
    all_code = []

    for p_code in paragraphs_code:
        if p_code.find('font') is not None:
            all_code.append([unicodedata.normalize("NFKD", p_code.get_text())])

    return all_code


def tag_visible(element) -> bool:
    """
    Проверяет, является ли элемент HTML видимым на странице.

    :param element: HTML-элемент.
    :return: True, если элемент видимый, иначе False.
    """
    if element.parent.name in ['style', 'script', 'head', 'title', 'meta', '[document]']:
        return False
    if isinstance(element, Comment):
        return False
    return True


def text_from_html(body: str) -> str:
    """
    Извлекает основной текст страницы, исключая ненужные элементы.

    :param body: HTML-код страницы.
    :return: Очищенный текст страницы.
    """
    bs = BeautifulSoup(body, 'html.parser')
    texts = bs.find_all(string=True)
    visible_texts = list(filter(tag_visible, texts))
    page_full_text = ' '.join(t.strip() for t in visible_texts)

    see_more_idx = page_full_text.find("См. также:")
    fore_ver_copyright = page_full_text[page_full_text.find("Справочная система на версию"):]

    if see_more_idx != -1:
        page_full_text = page_full_text[:see_more_idx] + fore_ver_copyright

    return page_full_text


def find_header(body: str) -> str:
    """
    Извлекает заголовок страницы.

    :param body: HTML-код страницы.
    :return: Заголовок страницы или стандартный заголовок "Документация Fore".
    """
    bs = BeautifulSoup(body, 'html.parser')
    header = bs.find("h1")

    if header:
        return header.text

    title = bs.find("title")
    return title.text if title else "Документация Fore"


def find_version(body: str) -> str:
    """
    Извлекает версию платформы из текста страницы.

    :param body: Текст страницы.
    :return: Версия платформы или пустая строка, если версия не найдена.
    """
    version_match = regex.findall(r'система на версию .{1,4}', body)
    return version_match[0].split()[-1] if version_match else ""


def collect_foresight_docs(sites: List[str]) -> List[Dict[str, str]]:
    """
    Собирает документацию с заданных веб-страниц.

    :param sites: Список URL-адресов страниц документации.
    :return: Список словарей с разделами документации, их текстами и версиями платформы.
    """
    results = []

    for url in sites:
        result = {}
        try:
            response = requests.get(url)
            response.raise_for_status()
            page_text = response.text

            result["Раздел документации"] = find_header(page_text)
            result["Текст раздела"] = text_from_html(page_text)
            result["Версия платформы"] = find_version(result["Текст раздела"])
        except requests.RequestException as ex:
            logger.error(f"Ошибка при запросе {url}: {ex}")

        results.append(result)

    return results
