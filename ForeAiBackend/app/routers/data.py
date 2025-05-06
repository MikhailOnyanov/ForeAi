import logging

from fastapi import APIRouter, HTTPException, Request
from fastapi.encoders import jsonable_encoder
from starlette.responses import JSONResponse

from ..constants import chroma_service_config
from ..services.vector_db_provider import VectorDBProvider
from ..models.collections import CollectionCreate, CollectionPublic

logger = logging.getLogger(__name__)

router = APIRouter(
    prefix="/data",
    tags=["data"]
)


@router.get('/collection_info')
def peek_data(collection_name: str):
    try:
        db_service = VectorDBProvider.get_vector_db_service("chroma", chroma_service_config)
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
def list_collections(request: Request):
    try:
        vector_db = request.app.state.vector_db
        if not vector_db:
            return JSONResponse(content=jsonable_encoder("Chroma is down"), status_code=503,
                                media_type="application/json")
        info = vector_db.list_collections()
        return JSONResponse(content=jsonable_encoder(info), status_code=200, media_type="application/json")
    except Exception as ex:
        logger.exception(f"Exception message: {ex}")
        raise HTTPException(status_code=500, detail=f"Exception: {ex}")

@router.post('/create_collection/', response_model=CollectionPublic)
def create_collection(collection: CollectionCreate, request: Request):
    try:
        vector_db = request.app.state.vector_db
        if not vector_db:
            return JSONResponse(content=jsonable_encoder("Chroma is down"), status_code=500, media_type="application/json")
        if vector_db.create_collection(collection.collection_name):
            return JSONResponse(content=jsonable_encoder(collection), status_code=201, media_type="application/json")
        else:
            return JSONResponse(
                content=f"Collection with name {collection} exists!",
                status_code=409, media_type="application/json")
    except Exception as ex:
        raise HTTPException(status_code=500, detail=f"Exception: {ex}")