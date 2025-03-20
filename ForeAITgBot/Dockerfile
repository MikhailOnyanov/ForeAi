FROM python:3.12-slim-bookworm
LABEL authors="MikhailOnyanov"

WORKDIR /code


COPY ./requirements.txt /code/requirements.txt


RUN pip install --no-cache-dir --upgrade -r /code/requirements.txt


COPY . /code/app


CMD ["python3.12", "app/main.py"]