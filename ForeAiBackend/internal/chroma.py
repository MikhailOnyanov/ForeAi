import chromadb
from chromadb.api.models.Collection import Collection


def get_chroma_collection(collection_name: str) -> Collection:
    try:
        client  = chromadb.HttpClient("localhost", 8001)
        collection: Collection = client.get_or_create_collection(name=collection_name)
        return collection
    except Exception as e:
        print(e)
        return None