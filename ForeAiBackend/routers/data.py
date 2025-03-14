from chromadb.api.models import Collection
from fastapi import APIRouter, HTTPException
from fastapi.encoders import jsonable_encoder
from starlette.responses import JSONResponse

from ..internal.chroma import get_chroma_collection

router = APIRouter(
    prefix="/data",
    tags=["data"]
)

@router.get('/test')
def peek_chroma_data2():
    print(1)
    return JSONResponse(content="Alive!", status_code=200, media_type="application/json")

@router.get('/collection_info')
def peek_chroma_data(collection_name: str):
        try:
            print(collection_name)
            collection: Collection = get_chroma_collection(collection_name)
            if not collection:
                return JSONResponse(content=jsonable_encoder("Col is down"), status_code=503, media_type="application/json")
            info = {
                'collection_name': collection_name,
                'element_count': collection.count(),
                'top_10_elements': str(collection.peek().values()),
            }
            return JSONResponse(content=jsonable_encoder(info), status_code=200, media_type="application/json")
        except KeyError:
            raise HTTPException(status_code=404, detail=f"Collection {collection_name} not found")