from __future__ import annotations
from flask import current_app
from evallapp.db import Base, db_session

from .xlsx.xlsx_operations import LineRecord
from sqlalchemy import select

from evallapp.importers.constants import MISTAKES_TYPES_TEMPLATE
# from database_connection import SQLiteConnection
from evallapp.models.core import *


class DatabaseCRUD:
    def __init__(self, s):
        self.db_session = db_session

    def add_work(self, year: str, code: int) -> None:
        work_object = Works(year=year, code=code)
        self.session_add(work_object)

    def add_mistake_type(self, mistake_type_id: int, mistake_type_transcript: str) -> None:
        mistake_type = MistakesTypes(
            mistake_type_id=mistake_type_id,
            mistake_type_transcript=mistake_type_transcript
        )
        self.session_add(mistake_type)

    def add_mistake_code(self,
                         mistake_type_id: int,
                         mistake_code: str,
                         mistake_code_transcript: str
                         ) -> None:
        mistake_code = MistakesCodes(
            mistake_type_id=mistake_type_id,
            mistake_code=mistake_code,
            mistake_code_transcript=mistake_code_transcript
        )
        self.session_add(mistake_code)

    def add_mistake_count(self,
                          work_id: int,
                          mistake_code_id: int,
                          mistakes_count: int
                          ) -> None:
        works_mistakes_count = WorksMistakes(
            work_id=work_id,
            mistake_code_id=mistake_code_id,
            mistakes_count=mistakes_count
        )
        self.session_add(works_mistakes_count)

    def init_mistake_types(self):
        mistakes_types: list[MistakesTypes] = []
        for key in MISTAKES_TYPES_TEMPLATE:
            mistake_type = MistakesTypes(
                mistake_type_id=MISTAKES_TYPES_TEMPLATE[key],
                mistake_type_transcript=key
            )
            mistakes_types.append(mistake_type)
        for elem in mistakes_types:
            if self.session_add(elem):
                current_app.logger.info(f"Added {mistakes_types} to DB.")

    def session_add(self, usr_obj: Base) -> bool:
        try:
            db_session.add(usr_obj)
            db_session.commit()
        except Exception as ex:
            current_app.logger.error(f"Failed to add: '{usr_obj}'.\nException message: \n{60 * '#'}\n{ex}\n{60 * '#'}")
            return False
        else:
            current_app.logger.info(f"Added: {usr_obj}")
            return True

    def add_sheet_data_to_db(self, lines: list[LineRecord]):
        # get all mistakes
        for line_record in lines:
            # add work to db
            try:
                work: Works = line_record.work
                db_session.add(work)
                # временно добавляем работу в БД, чтобы подвязать к ней ошибки
                db_session.flush()
                # TODO: если работа уже найдена в бд, то обновить данные
                # mistake_record уже приходит с записью о кол-во ошибок и её названии
                # в цикле ищем id ошибки по названию в mistakes_list, подвязываем его
                for mistake_record in line_record.mistakes:
                    mistake_record.work_code = work.work_code
                    # TODO: пересмотреть класс, мб сделать FK не id
                    try:
                        mistake_code_from_db = (db_session.scalars(
                            select(MistakesCodes)
                            .where(
                                MistakesCodes.mistake_code == mistake_record.mistake_code_raw
                            )).first()).mistake_code
                        mistake_record.mistake_code = mistake_code_from_db
                        db_session.add(mistake_record)
                    except Exception as ex:
                        current_app.logger.error(f"Problem occurred while working with {mistake_record}:\n{ex}")
                        db_session.rollback()
                db_session.commit()
            except Exception as ex:
                current_app.logger.error(f"Problem occurred while working with LineRecord obj:\n{ex}")
                db_session.rollback()

    def get_mistakes_list(self) -> list[MistakesCodes]:
        try:
            mistakes_list = db_session.scalars(select(MistakesCodes)).all()
            return mistakes_list
        except Exception as ex:
            current_app.logger.warning(ex)
