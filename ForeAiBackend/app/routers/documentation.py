import json

from fastapi import APIRouter
from fastapi.encoders import jsonable_encoder
from starlette.responses import JSONResponse
from starlette.requests import Request

from app.dependencies import ChromaServiceDep

from ..services.vector_db_provider import VectorDBProvider
from ..constants import test_sites
from ..services.parse_foresight_docs import collect_foresight_docs
import logging

logger = logging.getLogger(__name__)

router = APIRouter(
    prefix="/docs",
    tags=["docs"]
)



@router.get('/process_documentation')
def process_documentation_to_collection(vector_db: ChromaServiceDep, collection_name: str, save_locally: bool = True):
    try:
        docs: list[dict] = collect_foresight_docs(test_sites)
        if save_locally:
            with open("parsed_data/docs.json", "w") as file:
                json.dump(docs, file, ensure_ascii=False)
        if not vector_db:
            return JSONResponse(content=jsonable_encoder("Col is down"), status_code=503, media_type="application/json")
        vector_db.add_to_collection(docs, collection_name)
        return JSONResponse(content=jsonable_encoder(docs), status_code=200, media_type="application/json")
    except Exception as ex:
        logger.exception(ex)
        return JSONResponse(content=jsonable_encoder(ex), status_code=401, media_type="application/json")


@router.get('/get_vector')
def get_vector(vector_db: ChromaServiceDep, collection_name: str, message: str):
    logger.info(f"GETTING VECTORS FOR {message}")
    if not vector_db:
        vector_db = VectorDBProvider.get_vector_db_service("chroma", chroma_service_config)
        if not vector_db:
            return JSONResponse(content=jsonable_encoder("Col is down"), status_code=503, media_type="application/json")
    query_params = {'n_results': 3, 'query_texts': [message]}
    db_results = vector_db.query_collection(collection_name, query_params)
    text_res = []
    for corpus in zip(db_results["documents"], db_results["metadatas"]):
        text_res.append(corpus)

    return JSONResponse(content=jsonable_encoder(text_res), status_code=200,
                        media_type="application/json",
                        headers={"charset": "utf-8"})
