FROM python:3.11.5

WORKDIR /app

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

ARG ENV_FILE
COPY ${ENV_FILE} .env

COPY . .
