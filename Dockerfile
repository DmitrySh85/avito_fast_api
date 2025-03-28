FROM python:3.11-alpine

ARG UID=1000
ARG GID=1000

RUN addgroup -g ${GID} prod && \
    adduser -u ${UID} -G prod -s /bin/sh -D prod

WORKDIR /avito_fast_api

RUN chown -R ${GID}:${UID} /avito_fast_api && chmod 755 /avito_fast_api

COPY ./avito_fast_api/requirements.txt .

RUN pip install --no-cache-dir -r requirements.txt

COPY --chown={GID}:{UID} ./avito_fast_api .