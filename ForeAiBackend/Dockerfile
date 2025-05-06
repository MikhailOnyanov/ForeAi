FROM python:3.12-slim-bookworm
LABEL authors="MikhailOnyanov"

# Копируем бинарники uv
COPY --from=ghcr.io/astral-sh/uv:latest /uv /uvx /bin/

# Устанавливаем рабочую директорию
WORKDIR /code

# Копируем зависимости
COPY ./requirements.txt /code/requirements.txt

# Копируем конфиг логирования
COPY ./log_conf.yaml /code/log_conf.yaml

# Устанавливаем зависимости
RUN uv pip install --system -r /code/requirements.txt

# Копируем исходный код (если volume не используется)
COPY ./app /code/app

# Команда запуска: Uvicorn с hot reload
CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "80", "--reload", "--log-config", "log_conf.yaml"]