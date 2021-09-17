FROM python:3-slim

RUN useradd -m worker
USER worker

COPY --chown=worker:worker . /home/worker/app
WORKDIR /home/worker/app

RUN pip install --upgrade pip
RUN pip install --user requests

ENV PATH="/home/worker/.local/bin:${PATH}"


ENV PYTHONPATH /home/worker/app
CMD ["/home/worker/app/main.py"]
