from fastapi import APIRouter, HTTPException
from fastapi.encoders import jsonable_encoder
from starlette.responses import JSONResponse

from ..constants import client_info
from ..services.vector_db_provider import VectorDBProvider

router = APIRouter(
    prefix="/data",
    tags=["data"]
)


@router.get('/collection_info')
def peek_data(collection_name: str):
    try:
        db_service = VectorDBProvider.get_vector_db_service("chroma", client_info)
        if not db_service:
            return JSONResponse(content=jsonable_encoder("Vector database is down"), status_code=503,
                                media_type="application/json")
        info = db_service.get_collection_info(collection_name)
        return JSONResponse(content=jsonable_encoder(info), status_code=200, media_type="application/json")
    except KeyError:
        raise HTTPException(status_code=404, detail=f"Collection {collection_name} not found")
    except Exception as ex:
        raise HTTPException(status_code=500, detail=f"Exception: {ex}")

@router.get('/list_collections')
def list_collections():
    try:
        db_service = VectorDBProvider.get_vector_db_service("chroma", client_info)
        if not db_service:
            return JSONResponse(content=jsonable_encoder("Chroma is down"), status_code=503,
                                media_type="application/json")
        info = db_service.list_collections()
        return JSONResponse(content=jsonable_encoder(info), status_code=200, media_type="application/json")
    except Exception as ex:
        raise HTTPException(status_code=500, detail=f"Exception: {ex}")