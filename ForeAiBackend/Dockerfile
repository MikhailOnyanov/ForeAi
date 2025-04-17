FROM python:3.12-slim-bookworm
LABEL authors="MikhailOnyanov"
COPY --from=ghcr.io/astral-sh/uv:latest /uv /uvx /bin/

WORKDIR /code


COPY ./requirements.txt /code/requirements.txt


RUN uv pip install --system -r /code/requirements.txt


COPY ./app /code/app


CMD ["fastapi", "run", "app/main.py", "--port", "80"]