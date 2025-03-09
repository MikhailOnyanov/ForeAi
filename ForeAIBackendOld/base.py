from flask import (
    Blueprint, render_template, jsonify
)
from .utils import *
import random

bp = Blueprint('base', __name__)


@bp.route('/')
def base():
    tables = get_database_tables_names() or []
    return render_template('index.html', list=tables)

@bp.route('/fps')
def fps():
    the_answer = random.randint(25, 60)
    return jsonify(the_answer)

@bp.route('/view-queries-page')
def query_table():
    views = get_database_views_names() or []
    return render_template('view-queries-page.html', list=views)


@bp.route('/charts')
def charts():
    views = get_database_views_names() or []
    return render_template('charts-and-diagrams-page.html', list=views)
