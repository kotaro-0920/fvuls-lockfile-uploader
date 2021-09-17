FROM python:3-slim

RUN pip install --upgrade pip

RUN adduser -D worker
USER worker

COPY --chown=worker:worker . /home/worker/app
WORKDIR /home/worker/app

# We are installing a dependency here directly into our app source dir
RUN pip install --user --target=/home/worker/app requests

ENV PATH="/home/worker/.local/bin:${PATH}"


ENV PYTHONPATH /home/worker/app
CMD ["/app/main.py"]
