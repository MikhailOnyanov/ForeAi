from typing import Any
from .foresight_documentation_page import ForesightDoc

# def parse_chromadb_query_to_foresight_documents(chromadb_query_result: dict[Any]) -> list[Fore]:
#     # "Раздел документации": doc["Раздел документации"],
#     # "Версия платформы": doc["Версия платформы"]
#     aligned_documents = dict(zip(chromadb_query_result['metadatas'], chromadb_query_result['documents']))
#     print(aligned_documents)
#     pass

def parse_chromadb_query_to_foresight_documents_old(db_results: dict[Any]) -> list:
    text_res = []
    for doc_l, meta_l in zip(db_results["documents"], db_results["metadatas"]):
        for doc, meta in zip(doc_l, meta_l):
            text_res.append(
                ForesightDoc(doc, meta["Версия платформы"], meta["Раздел документации"])
            )
    return text_res
