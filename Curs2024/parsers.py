import regex

import unicodedata
from bs4 import BeautifulSoup, Comment
import requests


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


url = 'https://help.fsight.ru/ru/mergedProjects/fore/02_generalinfo/fore_gening_const.htm'

response = requests.get(url)
bs = BeautifulSoup(response.text, "html.parser")


# text = get_simple_texts(bs)
# for t in text:
#     print(t)
# print("/////////////////////////")
# code = parse_code_blocks(bs)
# for c in code:
#     print(c)

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
