from pydantic import BaseModel, Field


class Collection(BaseModel):
    collection_name: str = Field(default='fore_collection', description='Name of the created collection')

class CollectionCreate(Collection):
    pass

class CollectionPublic(Collection):
    pass