import io

from sqlalchemy import inspect, Table, select, Row
from sqlalchemy.orm import DeclarativeMeta

from .models.core import *
from flask import current_app
from .db import engine, db_session, Base


def get_database_tables_names() -> list[str]:
    try:
        inspector = inspect(engine)
        schemas = inspector.get_schema_names()
        tables = []
        for schema in schemas:
            if schema != 'information_schema':
                for table_name in inspector.get_table_names(schema=schema):
                    tables.append(table_name)
                # for column in inspector.get_columns(table_name, schema=schema):
                # print("Column: %s" % column)
        current_app.logger.info(f"Returned: {tables}")
        return tables
    except Exception as ex:
        current_app.logger.error(ex)
        return []


def get_database_views_names() -> list[str]:
    views = []
    try:
        inspector = inspect(engine)
        for view_name in inspector.get_view_names():
            if view_name != 'pg_stat_statements':
                views.append(view_name)
        current_app.logger.info(f"Returned: {views}")
        return views
    except Exception as ex:
        current_app.logger.error(ex)
        return []


def get_table_by_name(db_name: str, prepare_columns: bool = False) -> dict | None:
    table_class = find_mapper_for_table(Base, db_name)
    try:
        res = db_session.scalars(select(table_class)).all()
        if res:
            table_data = {}
            table_keys: list[str] = list((res[0].to_dict()).keys())
            table_data["columns"] = table_keys
            table_data["data"] = []
            row_counter = 0

            for val in res:
                row_counter += 1
                obj: dict = val.to_dict()
                table_data["data"].append(obj)
            table_data["total"] = row_counter

            current_app.logger.info(
                f"Collected {row_counter} rows of '{table_class.__name__}' table."
            )
            if prepare_columns:
                table_data["columns"] = prepare_columns_gridjs_format(table_keys)
            return table_data
        else:
            return None
    except Exception as ex:
        current_app.logger.error(ex)


def get_view_by_name(view_name: str):
    view = Table(view_name, Base.metadata, autoload_with=engine)
    if view is not None:
        table_data = {}
        row_counter = 0

        table_keys: list[str] = []
        for column in view.columns:
            table_keys.append(column.key)
        table_data["columns"] = sorted(table_keys)

        table_data["data"] = []
        table_values: list[tuple] = db_session.query(view)
        for val in table_values:
            val = dict(val._mapping)
            table_data["data"].append(val)
            row_counter += 1
        table_data["total"] = row_counter
        current_app.logger.info(
            f"Collected {row_counter} rows of '{view_name}' view."
        )
        return table_data


def find_mapper_for_table(base_class: DeclarativeMeta, target_name: str) -> Base | None:
    d = {}
    for mapper in base_class.registry.mappers:
        cls = mapper.class_
        classname = cls.__name__
        if not classname.startswith('_'):
            table_name = cls.__tablename__
            d[table_name] = cls
    try:
        return d[target_name]
    except KeyError:
        current_app.logger.warning(f"Can't find mapper for {target_name}")
        return None
    except Exception as ex:
        current_app.logger.warning(f"Problems while finding mapper for {target_name}. {ex}")
        return None


def prepare_columns_gridjs_format(columns: list) -> list[dict]:
    result = []
    for title in columns:
        d = {}
        d["id"] = title
        # можно добавить предобработчик имён, чтобы кидать на фронт не "mistake_type_id", а "идентификатор ошибки"
        d["name"] = title
        result.append(d)
    return result


def update_data_for_mapped_table(table_name: str, key: str, data_to_change: dict):
    try:
        t = find_mapper_for_table(Base, table_name)
        mapped_object = db_session.query(t).get(key)
        current_app.logger.info(f"Found mapper for {table_name}")
        atr_key = list(data_to_change.keys())[0]
        data_to_write = data_to_change[atr_key]
        setattr(mapped_object, atr_key, data_to_write)
        db_session.commit()
        current_app.logger.info(f"Committed changes to {table_name}")
    except Exception as ex:
        current_app.logger.info(f"Unpredicted error {ex}")


def delete_data_from_table(table_name: str, key: str):
    try:
        t = find_mapper_for_table(Base, table_name)
        mapped_object = db_session.query(t).get(key)
        current_app.logger.info(f"Found mapper for {table_name}")
        db_session.delete(mapped_object)
        db_session.commit()
        current_app.logger.info(f"Committed changes to {table_name}. Deleted {mapped_object}")
    except Exception as ex:
        current_app.logger.info(f"Unpredicted error {ex}")
