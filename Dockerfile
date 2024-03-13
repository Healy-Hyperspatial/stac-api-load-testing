FROM python:3.10-slim-buster
WORKDIR /code
COPY . /code/

RUN pip install . && \
    stac-api-load-testing --help

ENTRYPOINT ["stac-api-load-testing"]