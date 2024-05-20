#------------------------------------------
#----------------FLASK-------------------
#------------------------------------------

#FROM python:3.9-slim-buster

#RUN groupadd -g 999 python \
#    && useradd -r -u 999 -g python python \
#    && mkdir -p /usr/app \
#    && python -m venv /usr/app/.venv \
#    && chown -R python:python /usr/app 

#ENV PATH="/usr/app/.venv/bin:$PATH"
#ENV PIP_NO_CACHE_DIR=off

#WORKDIR /usr/app

#USER 999
#COPY --chown=python:python requirements.txt requirements.txt
#RUN pip install --upgrade pip && \
#    pip install -r requirements.txt

#COPY main_flask.py main_flask.py

#EXPOSE 8080

#CMD ["python", "main_flask.py"]

#------------------------------------------
#----------------FASTAPI-------------------
#------------------------------------------

FROM python:3.10.10

USER root

ENV POETRY_VERSION="1.3.2"

RUN pip install "poetry==$POETRY_VERSION"
RUN pip install psycopg2-binary

WORKDIR /code

RUN poetry config virtualenvs.create false

COPY poetry.lock pyproject.toml /code/

RUN poetry install --no-interaction --no-ansi

COPY ./app /code/app

CMD ["poetry", "run", "uvicorn", "main_fastapi:app", "--port", "8000", "--host", "0.0.0.0", "--reload"]