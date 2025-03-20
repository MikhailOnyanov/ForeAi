from fastapi import APIRouter
from fastapi.encoders import jsonable_encoder
from starlette.responses import JSONResponse

from ..services.vector_db_provider import VectorDBProvider
from ..constants import test_sites, client_info
from ..services import parse_foresight_docs
from ..dependencies import logger

router = APIRouter(
    prefix="/docs",
    tags=["docs"]
)



@router.get('/process_documentation')
def process_documentation_to_collection(collection_name: str):
    try:
        docs: list[dict] = parse_foresight_docs.collect_foresight_docs(test_sites)
        db_service = VectorDBProvider.get_vector_db_service("chroma", client_info)
        if not db_service:
            return JSONResponse(content=jsonable_encoder("Col is down"), status_code=503, media_type="application/json")
        db_service.add_to_collection(docs, collection_name)
        return JSONResponse(content=jsonable_encoder(docs), status_code=200, media_type="application/json")
    except Exception as ex:
        logger.exception(ex)
        return JSONResponse(content=jsonable_encoder(ex), status_code=401, media_type="application/json")


@router.get('/get_vector')
def get_vector(collection_name: str, message: str):
    logger.info(f"GETTING VECTORS FOR {message}")
    db_service = VectorDBProvider.get_vector_db_service("chroma", client_info)
    if not db_service:
        return JSONResponse(content=jsonable_encoder("Col is down"), status_code=503, media_type="application/json")
    query_params = {'n_results': 3, 'query_texts': [message]}
    db_results = db_service.query_collection(collection_name, query_params)
    text_res = []
    for corpus in zip(db_results["documents"], db_results["metadatas"]):
        text_res.append(corpus)

    return JSONResponse(content=jsonable_encoder(text_res), status_code=200,
                        media_type="application/json",
                        headers={"charset": "utf-8"})
