FROM python:3.10-slim AS builder
ADD . /app
WORKDIR /app

# We are installing a dependency here directly into our app source dir
RUN python -m venv /venv && \
    /venv/bin/pip install --upgrade pip && \
    /venv/bin/pip install requests validators


FROM gcr.io/distroless/python3-debian10
COPY --from=builder /venv /venv
COPY --from=builder /app /app
WORKDIR /app

# デフォルトPythonにvenvを使わせる
ENV PYTHONHOME=/venv
CMD ["/venv/bin/python", "/app/main.py"]
