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

CMD ["poetry", "run", "uvicorn", "app.main:app", "--port", "8000", "--host", "0.0.0.0", "--reload"]