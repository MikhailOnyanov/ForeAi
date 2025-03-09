import json
from .constants import test_sites
from flask import (Blueprint, request, jsonify, Response)
from .documentation_collector import collect_docs
from .db import fore_collection
from dict_hash import dict_hash

bp = Blueprint('api_v1', __name__, url_prefix='/apiv1')


@bp.route('/process_documentation', methods=['POST'])
def fetch_dataset():
    data = request.get_json()
    if 'sites' not in data:
        sites = test_sites
    else:
        sites = data['sites']

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


@bp.route('/get_vector', methods=['GET'])
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
