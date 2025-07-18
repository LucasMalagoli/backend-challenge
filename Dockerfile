FROM python:3.11-slim

WORKDIR /code

COPY requirements.txt .
RUN apt-get update && apt-get install -y netcat-openbsd \
    && rm -rf /var/lib/apt/lists/*
RUN pip install --no-cache-dir -r requirements.txt

COPY ./app ./app
COPY entrypoint.sh .
COPY alembic.ini .
COPY alembic ./alembic

CMD ["./entrypoint.sh"]
