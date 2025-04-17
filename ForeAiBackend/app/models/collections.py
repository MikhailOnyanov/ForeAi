from pydantic import BaseModel

class Collection(BaseModel):
    collection_name: str

class CollectionCreate(Collection):
    pass

class CollectionPublic(Collection):
    pass