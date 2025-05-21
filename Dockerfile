FROM python:3.10-slim

WORKDIR /app
COPY . /app

# もしrequests, validatorsを入れたいなら
RUN pip install --no-cache-dir requests validators

CMD ["python", "/app/main.py"]
