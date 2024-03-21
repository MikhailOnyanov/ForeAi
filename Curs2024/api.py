import io
import json

from flask import (
    Blueprint, request, current_app, jsonify, abort, make_response, send_file, Response
)
from .documentation_collector import collect_docs

bp = Blueprint('api_v1', __name__, url_prefix='/apiv1')


@bp.route('/process_documentation', methods=['POST'])
def fetch_dataset():
    data = request.get_json()
    if 'sites' not in data:
        sites = ['https://help.fsight.ru/ru/mergedProjects/fore/02_generalinfo/fore_gening_const.htm',
                 'https://help.fsight.ru/ru/mergedProjects/fore/06_syntrules/fore_synt_visible.htm',
                 'https://help.fsight.ru/9.9/ru/mergedProjects/Assembly/System_Assembly.htm',
                 'https://help.fsight.ru/9.9/ru/mergedProjects/kedims/kedims_title.htm',
                 'https://help.fsight.ru/9.9/ru/mergedProjects/kedims/class/kedims_class.htm',
                 'https://help.fsight.ru/9.9/ru/mergedProjects/kedims/interface/idimtextcriteria/idimtextcriteria.text.htm']
    else:
        sites = data['sites']

    docs: list[dict] = collect_docs(sites)

    if len(docs) > 0:
        return Response(response=json.dumps(docs, ensure_ascii=False).encode('utf8'), status=200, mimetype="application/json",
                        headers={"charset": "utf-8"})
    else:
        return Response(response={}, status=401, mimetype="application/json")


@bp.route('/get_vector', methods=['GET'])
def get_vector():
    msg = request.args.get('message')
    print(msg)
    return jsonify(f"hi: {msg}")
