import chromadb
from chromadb import Collection
import logging

from ..services.base_vector_db_service import BaseVectorDBService
from ..services.hashing_service import HashingService


class ChromaService(BaseVectorDBService):
    def __init__(self, client_info: dict):
        self.client_info = client_info
        self.client = self.init_client(client_info)

    @staticmethod
    def init_client(client_info: dict):
        if client_info.get('client_type', None) == 'http':
            logging.info(f"Connecting to chroma server with creds: {client_info.get('client_kwargs')}")
            return chromadb.HttpClient(**client_info.get('client_kwargs'))
        else:
            raise NotImplementedError(f'Type {client_info.get('client_type', None)} is not implemented.')

    def get_collection(self, collection_name: str) -> Collection | None:
        try:
            collection = self.client.get_collection(collection_name)
            logging.info(f'Get collection {collection_name} sucess')
            return collection
        except Exception as ex:
            logging.warning(f'Get collection {collection_name} failed: {ex}')
            return None

    def get_collection_info(self, collection_name: str) -> dict | None:
        collection = self.get_collection(collection_name)
        if collection:
            return {
                'collection_name': collection_name,
                'element_count': collection.count(),
                'top_10_elements': str(collection.peek().values()),
            }
        else:
            return None

    def query_collection(self, collection_name: str, query_params: dict) -> dict:
        collection = self.get_collection(collection_name)
        results = collection.query(**query_params, include=["documents", "metadatas"])
        return results

    def add_to_collection(self, docs: list[dict], collection_name: str):
        collection = self.get_collection(collection_name)
        if len(docs) > 0:
            for doc in docs:
                collection.add(
                    documents=[doc["Текст раздела"]],
                    metadatas=[
                        {
                            "Раздел документации": doc["Раздел документации"],
                            "Версия платформы": doc["Версия платформы"]
                        }
                    ],
                    ids=[str(HashingService.dict_hash(doc))]
                )

    def list_collections(self):
        return self.client.list_collections()