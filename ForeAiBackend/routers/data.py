from chromadb.api.models import Collection
from fastapi import APIRouter, HTTPException
from fastapi.encoders import jsonable_encoder
from starlette.responses import JSONResponse

from ..constants import client_info
from ..services.vector_db_provider import VectorDBProvider
from ..internal.chroma import get_chroma_collection

router = APIRouter(
    prefix="/data",
    tags=["data"]
)


@router.get('/collection_info')
def peek_chroma_data(collection_name: str):
        try:
            db_service = VectorDBProvider.get_vector_db_service("chroma", client_info)
            if not db_service:
                return JSONResponse(content=jsonable_encoder("Col is down"), status_code=503,
                                    media_type="application/json")
            info = db_service.get_collection_info(collection_name)
            return JSONResponse(content=jsonable_encoder(info), status_code=200, media_type="application/json")
        except KeyError:
            raise HTTPException(status_code=404, detail=f"Collection {collection_name} not found")