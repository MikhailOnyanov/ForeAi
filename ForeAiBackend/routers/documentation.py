from fastapi import APIRouter
from ..dependencies import fore_collection, collect_docs, test_sites

router = APIRouter()


@router.get("/users/", tags=["users"])
async def read_users():
    return [{"username": "Rick"}, {"username": "Morty"}]


@router.get("/users/me", tags=["users"])
async def read_user_me():
    return {"username": "fakecurrentuser"}


@router.post('/process_documentation', tags=["documentation"])
def fetch_dataset():

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

        return Response(response=json.dumps(docs, ensure_ascii=False).encode('utf8'), status=200,
                        mimetype="application/json",
                        headers={"charset": "utf-8"})
    else:
        return Response(response={}, status=401, mimetype="application/json")


@router.get('/get_vector')
def get_vector():
    msg = request.args.get('message')
    bd_results = fore_collection.query(
        query_texts=[msg],
        n_results=3)

    text_res = []

    for corpus in zip(bd_results["documents"], bd_results["metadatas"]):
        text_res.append(corpus)

    return Response(response=json.dumps(text_res, ensure_ascii=False).encode('utf8'), status=200,
                        mimetype="application/json",
                        headers={"charset": "utf-8"})
