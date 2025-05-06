from .common import get_chroma_creds
from typing import Annotated
from fastapi import Depends

test_sites = ['https://help.fsight.ru/ru/mergedProjects/fore/02_generalinfo/fore_gening_const.htm',
              'https://help.fsight.ru/ru/mergedProjects/fore/06_syntrules/fore_synt_visible.htm',
              'https://help.fsight.ru/9.9/ru/mergedProjects/Assembly/System_Assembly.htm',
              'https://help.fsight.ru/9.9/ru/mergedProjects/kedims/kedims_title.htm',
              'https://help.fsight.ru/9.9/ru/mergedProjects/kedims/class/kedims_class.htm',
              'https://help.fsight.ru/9.9/ru/mergedProjects/kedims/interface/idimtextcriteria/idimtextcriteria.text.htm']

chroma_service_config = {
    "client_type": "http",
    "client_kwargs": {"host": "chroma-server", "port": 8000},
}