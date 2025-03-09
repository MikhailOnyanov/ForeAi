from flask import Flask, render_template, Blueprint, flash
from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField
from wtforms.validators import DataRequired, Email
from .models.core import *
from .db import db_session

bp = Blueprint('form', __name__)


# Create Form Class
class MistakeTypeForm(FlaskForm):
    title = StringField("Email", validators=[DataRequired(), Email()])
    submit = SubmitField("Создать")


# Create Type page
@bp.route('/notifications', methods=['GET', 'POST'])
def notifications():
    title = None
    error_flag = False
    form = MistakeTypeForm()

    # Validate form
    print(form.validate_on_submit())

    if form.is_submitted():
        if form.validate():
            title = form.title.data
            form.title.data = ''
            # Logic for appending data
            try:
                new_mistake_type = MistakesTypes()
                new_mistake_type.mistake_type_transcript = title
                db_session.add(new_mistake_type)
                db_session.commit()
                flash(f"Запись успешно создана: {new_mistake_type} в БД")
            except Exception as ex:
                error_flag = True
                flash(f"Ошибка добавления записи: {ex}")
        else:
            flash(f"Введите корректный почтовый адрес формата: example@example.com")

    return render_template("form-create-mistake-type.html",
                           title=title,
                           form=form,
                           error_flag=error_flag)
