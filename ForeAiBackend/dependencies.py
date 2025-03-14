import regex

import unicodedata
from bs4 import BeautifulSoup, Comment
import requests

from typing import Dict, Any
import hashlib
import json


def get_simple_texts(bs_instance: BeautifulSoup) -> list:
    paragraphs_all = bs_instance.findAll('p')
    simple_text = []
    for p in paragraphs_all:
        if len(p.attrs) == 0:
            simple_text.append(p)
    return simple_text


def parse_code_blocks(bs_instance: BeautifulSoup) -> list:
    paragraphs_code = bs_instance.findAll('p', attrs={'style': 'font-family: \'Courier New\'; font-size: 10pt;'})

    all_code = []
    for p_code in paragraphs_code:
        filtered_code = []
        if p_code.find('font') is not None:
            filtered_code.append(unicodedata.normalize("NFKD", p_code.text))
        all_code.append(filtered_code)

    return all_code


def tag_visible(element):
    if element.parent.name in ['style', 'script', 'head', 'title', 'meta', '[document]']:
        return False
    if isinstance(element, Comment):
        return False
    return True


def text_from_html(body):
    bs = BeautifulSoup(body, 'html.parser')
    texts = bs.findAll(string=True)
    visible_texts = list(filter(tag_visible, texts))
    new_t = u" ".join(t.strip() for t in visible_texts)
    page_full_text = ' '.join(new_t.split())

    see_more_idx = page_full_text.find("См. также:")
    fore_ver_copyright = page_full_text[page_full_text.find("Справочная система на версию"):]
    page_full_text = page_full_text[:see_more_idx] + fore_ver_copyright
    return page_full_text


def find_header(body):
    bs = BeautifulSoup(body, 'html.parser')
    header = bs.find("h1")
    if header is None:
        header_from_root = bs.find("title")
        if header_from_root is None:
            return "Документация Fore"
        else:
            return header_from_root.text
    return header.text


def find_version(body):
    version = regex.findall('система на версию .{1,4}', body)[0].split()
    if version:
        return version[-1]
    else:
        return ""

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


def dict_hash(dictionary: Dict[str, Any]) -> str:
    """MD5 hash of a dictionary."""
    dhash = hashlib.md5()
    encoded = json.dumps(dictionary, sort_keys=True).encode()
    dhash.update(encoded)
    return dhash.hexdigest()