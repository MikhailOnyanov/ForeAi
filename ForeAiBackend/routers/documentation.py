from fastapi import APIRouter
from fastapi.encoders import jsonable_encoder
from starlette.responses import JSONResponse

from ..internal.chroma import get_chroma_collection
from ..dependencies import collect_docs, dict_hash
from ..constants import test_sites


router = APIRouter(
    prefix="/docs",
    tags=["docs"]
)



@router.get('/process_documentation')
def fetch_dataset():
    fore_collection = get_chroma_collection("fore_collection")
    if not fore_collection:
        return JSONResponse(content=jsonable_encoder("Col is down"), status_code=503, media_type="application/json")
    sites = test_sites

    docs: list[dict] = collect_docs(sites)

    if len(docs) > 0:

        for doc in docs:
            fore_collection.add(
                documents=[doc["Текст раздела"]],
                metadatas=[
                    {
                        "Раздел документации": doc["Раздел документации"],
                        "Версия платформы": doc["Версия платформы"]
                    }
                ],
                ids=[str(dict_hash(doc))]
            )

        return JSONResponse(content=jsonable_encoder(docs), status_code=200, media_type="application/json")
    else:
        return JSONResponse(content={}, status_code=401, media_type="application/json")


@router.get('/get_vector')
def get_vector(message: str):
    fore_collection = get_chroma_collection("fore_collection")
    if not fore_collection:
        return JSONResponse(content=jsonable_encoder("Col is down"), status_code=503, media_type="application/json")
    db_results = fore_collection.query(
        query_texts=[message],
        n_results=3)

    text_res = []

    for corpus in zip(db_results["documents"], db_results["metadatas"]):
        text_res.append(corpus)

    return JSONResponse(content=jsonable_encoder(text_res), status_code=200,
                        media_type="application/json",
                        headers={"charset": "utf-8"})
