import logging

import chromadb
from chromadb import Client, Collection

from app.conifg import ChromaConfig

from ..services.base_vector_db_service import BaseVectorDBService
from ..services.hashing_service import HashingService


logger = logging.getLogger(__name__)

class ChromaService(BaseVectorDBService):
    def __init__(self, client_config: ChromaConfig):
        self.client_config = client_config
        self.client: Client = self.init_client(client_config)

    def init_client(self, config: ChromaConfig):
        """В зависимости от типа клиента Chroma возвращает клиент для взаимодействия с VectorDB."""
        if config.CLIENT_TYPE == 'http':
            logger.info(
                f'Connecting to chroma server with creds: {config.HOST, config.PORT}')
            try:
                client = chromadb.HttpClient(host=config.HOST, port=config.PORT)
                logger.info(f'CHROMA Heartbeat: {client.heartbeat()}')
                return client
            except TimeoutError as ex:
                logger.exception(f'TIMEOUT WHILE CONNECTING TO CHROMA: {ex}')
                return None
        else:
            raise NotImplementedError(
                f'Type CLIENT_TYPE={config.CLIENT_TYPE} is not implemented.')

    def get_collection(self, collection_name: str) -> Collection | None:
        try:
            collection = self.client.get_collection(collection_name)
            logger.info(f'Get collection {collection_name} success')
            return collection
        except Exception:
            logger.warning(f'Collection {collection_name} does not exist!')
            return None

    def create_collection(self, collection_name: str) -> bool:
        try:
            self.client.create_collection(collection_name)
            return True
        # If collection exists
        except Exception:
            logger.info(f'Collection {collection_name} already exists')
            return False

    def get_collection_info(self, collection_name: str) -> dict | None:
        collection = self.get_collection(collection_name)
        if collection:
            return {
                'collection_name': collection_name,
                'element_count': collection.count(),
                'top_10_elements': str(collection.peek().values()),
            }
        return None

    def query_collection(self, collection_name: str, query_params: dict) -> dict:
        collection = self.get_collection(collection_name)
        results = collection.query(**query_params, include=['documents', 'metadatas'])
        return results

    def add_to_collection(self, docs: list[dict], collection_name: str):
        collection = self.get_collection(collection_name)
        if len(docs) > 0:
            for doc in docs:
                collection.add(
                    documents=[doc['Текст раздела']],
                    metadatas=[
                        {
                            'Раздел документации': doc['Раздел документации'],
                            'Версия платформы': doc['Версия платформы']
                        }
                    ],
                    ids=[str(HashingService.dict_hash(doc))]
                )

    def list_collections(self):
        return [c.name for c in self.client.list_collections()]