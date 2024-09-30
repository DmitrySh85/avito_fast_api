FROM python:3.11

RUN pip install --upgrade pip

RUN useradd -rms /bin/bash prod && chmod 777 /opt /run

WORKDIR /avito_fast_api

RUN chown -R prod:prod /avito_fast_api && chmod 755 /avito_fast_api

COPY ./avito_fast_api/requirements.txt .

RUN pip install -r requirements.txt

USER prod

COPY --chown=prod:prod ./avito_fast_api /avito_fast_api

RUN chmod +x /avito_fast_api/docker/app.sh