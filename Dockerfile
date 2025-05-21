FROM python:3.10-slim AS builder
WORKDIR /app
COPY . /app

RUN pip install --no-cache-dir -r requirements.txt

CMD ["python", "/app/main.py"]

