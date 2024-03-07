FROM python:3.10-slim-buster
WORKDIR /code
COPY . /code/

RUN pip install . && \
    stac-api-load-balancing --help

ENTRYPOINT ["stac-api-load-balancing"]