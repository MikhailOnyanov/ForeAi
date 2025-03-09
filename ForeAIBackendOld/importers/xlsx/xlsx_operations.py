from __future__ import annotations
from evallapp.importers.constants import MISTAKES_TYPES_TEMPLATE, MISTAKE_CODE_SYM, XLSX_MISTAKES_LOCATOR, WORKS_FIELD_NAMES
from evallapp.models.core import *
from . import validators
import pandas as pd
from pandas import DataFrame
from flask import current_app


class ExcelWorker:
    def __init__(self, xl_path):
        try:
            file = pd.ExcelFile(xl_path)
            self.xl = file
            self.sheet_names = self.xl.sheet_names
            current_app.logger.info(f"Created Excel object from {xl_path}. \nAvailable sheets: {self.sheet_names}\n")
        except Exception as ex:
            current_app.logger.error(f"Failed to create ExcelWorker. {ex}")

    def process_sheet(self, sheet_position) -> list[LineRecord]:
        """
        Processes data from Excel file to object collections
        """
        df = self.get_sheet_by_position(sheet_position)
        if df is not None:
            # TODO: optimise iterations
            rows_collection = []
            for index in range(XLSX_MISTAKES_LOCATOR, len(df)):
                line: pd.Series = df.iloc[index]
                # Working with row
                try:
                    work = self.get_work_from_line(line)
                    if work is not None:
                        res_mistakes = self.get_mistakes_from_line(line)
                        line_info = LineRecord(work=work, mistakes=res_mistakes)
                        rows_collection.append(line_info)
                except Exception as ex:
                    current_app.logger.error(f"Failed to process line {index}:\n{ex}")
            return rows_collection
        else:
            current_app.logger.info("Dataframe is empty")
            return None

    def get_sheets(self) -> list:
        return self.sheet_names

    def get_sheet_by_name(self, sheet_name) -> DataFrame | None:
        if sheet_name in self.sheet_names:
            return self.xl.parse(sheet_name)
        else:
            return None

    def get_sheet_by_position(self, pos) -> DataFrame | None:
        if pos - 1 < len(self.sheet_names):
            return self.xl.parse(self.sheet_names[pos])
        else:
            return None

    def get_mistakes_codes_from_list(self, sheet_position: int):
        # Инф-я об ошибках содержится до индекса константы (считывает с 0 до 2 строки)
        df = self.get_sheet_by_position(sheet_position).iloc[:XLSX_MISTAKES_LOCATOR]
        return self._get_mistakes_codes(df)

    # ожидаются первые 3 строки листа (код ошибки, описание и тип)
    # обрабатывает строку, в которой ключами ожидаются id ошибок ("06.03" и т.п.), а значением описание (любой текст)
    # нужен для обновления списка ошибок с их типами
    def _get_mistakes_codes(self, df: pd.DataFrame) -> list[MistakesCodes]:
        res = []
        for mistake_code in df.columns:
            if MISTAKE_CODE_SYM in mistake_code:
                # один из MISTAKES_TYPES_TEMPLATE
                mistake_type_name = df[mistake_code][1]
                mistake_type_id = MISTAKES_TYPES_TEMPLATE[mistake_type_name]
                mistake_code_transcript = df[mistake_code][0]
                try:
                    new_mistake = MistakesCodes(
                        mistake_type_id=mistake_type_id,
                        mistake_code=mistake_code.strip(),
                        mistake_code_transcript=mistake_code_transcript
                    )
                    res.append(new_mistake)
                except Exception as ex:
                    current_app.logger.error(f"Problem while getting mistakes codes:\n{ex}")
        return res

    # получает на вход строку из датафрейма
    # по шаблону имён WORKS_FIELD_NAMES ищет имена в строке
    # если находит, то устанавливает зн-ия объекту класса works
    def get_work_from_line(self, line: pd.Series) -> Works | None:
        try:
            work = Works()
            for key in WORKS_FIELD_NAMES:
                if hasattr(work, WORKS_FIELD_NAMES[key]):
                    val = line[key]
                    if WORKS_FIELD_NAMES[key] == "work_code":
                        val = int(val)
                    work.__setattr__(WORKS_FIELD_NAMES[key], val)
                else:
                    raise Exception(f"No attribute: {WORKS_FIELD_NAMES[key]}")
            current_app.logger.info(work)
            return work
        except Exception as ex:
            current_app.logger.error(ex)
            return None

    def get_mistakes_from_line(self, line: pd.Series) -> list[WorksMistakes]:
        try:
            result: list[WorksMistakes] = []
            for key in line.keys():
                if MISTAKE_CODE_SYM in key:
                    elem = WorksMistakes()
                    try:
                        mistake_raw = key
                        mistakes_count = int(line[key])
                    except Exception as ex:
                        #current_app.logger.warning(f"Can't read {key} from line:\n{ex}")
                        mistakes_count = 0
                    elem.mistakes_count = mistakes_count
                    elem.mistake_code_raw = mistake_raw
                    result.append(elem)
            return result
        except Exception as ex:
            current_app.logger.error(ex)
    # TODO: close file!
    def create_file_from_data(self, data: pd.DataFrame):
        pass


class LineRecord:
    def __init__(self, work: Works, mistakes: list[WorksMistakes]):
        self.work: Works = work
        self.mistakes: list[WorksMistakes] = mistakes

