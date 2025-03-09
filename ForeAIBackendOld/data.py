import io
from flask import (
    Blueprint, request, current_app, jsonify, abort, Response, send_file
)
from .utils import get_table_by_name, update_data_for_mapped_table, get_view_by_name, \
    delete_data_from_table

bp = Blueprint('data', __name__, url_prefix='/api')


@bp.route('/fetch_dataset', methods=['GET'])
def fetch_dataset():
    db_name = request.args.get('db_name')
    if db_name:
        table_values = get_table_by_name(db_name, prepare_columns=True)
        return jsonify(table_values)
    else:
        return "Dataset not found", 400


@bp.route('/fetch_view', methods=['GET'])
def fetch_view():
    db_name = request.args.get('db_name')
    if db_name:
        table_values = get_view_by_name(db_name)
        return jsonify(table_values)
    else:
        return "Dataset not found", 400


@bp.route('/data', methods=['POST'])
def update():
    data = request.get_json()
    if 'table_name' not in data:
        abort(400)
    try:
        table_name = data['table_name']
        key = data["id"]
        data_to_change = data['data']
        update_data_for_mapped_table(table_name, key, data_to_change)
        return Response(f"Изменения в '{table_name}' внесены: {key}:{data_to_change}", status=200,
                        mimetype='application/json')
    except Exception as ex:
        return Response(f"Текст ошибки: {ex}", status=500, mimetype='application/json')


@bp.route('/delete_row', methods=['POST'])
def delete_row():
    data = request.get_json()
    if 'table_name' not in data:
        abort(400)
    try:
        table_name = data['table_name']
        print(data.keys())
        key = data["id"]
        delete_data_from_table(table_name, key)
        return Response(f"Изменения в '{table_name}' внесены: Запись {key}: удалён", status=200,
                        mimetype='application/json')
    except Exception as ex:
        return Response(f"Текст ошибки: {ex}", status=500, mimetype='application/json')


@bp.route('/get_df_xlsx', methods=['GET'])
def get_df_xlsx():
    table_name = request.args.get('table_name')
    if not table_name:
        abort(400)
    try:
        file_bytes = get_table_data_xlsx(table_name)
        mimetype = 'application/vnd.openxmlformats-officedocument.spreadsheetml.sheet'
        return send_file(
            io.BytesIO(file_bytes),
            mimetype=mimetype,
            download_name='test.xlsx',
            as_attachment=True
        )
    except Exception as ex:
        current_app.logger.warning(f"Неизвестная ошибка при получении таблицы БД в формате Excel: {ex}")

