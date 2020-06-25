FROM python:3.8-alpine

ARG workdir=/var/www/surfacescan
ARG user=surfacescan
ARG poetry_opts=

WORKDIR ${workdir}

COPY pyproject.toml .
COPY poetry.lock .

RUN adduser -D ${user} \
    && chown -R ${user}:${user} ${workdir} \
    && apk add --virtual .build-deps musl-dev gcc libffi-dev openssl-dev make \
    && pip install poetry \
    && poetry config virtualenvs.create false \
    && poetry install ${poetry_opts} \
    && apk del .build-deps

USER ${user}
EXPOSE 8001

COPY . .

ENTRYPOINT [ "uvicorn", "surfacescan.main:app", "--port", "8001", "--host", "0.0.0.0" ]
