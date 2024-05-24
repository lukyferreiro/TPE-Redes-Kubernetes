#------------------------------------------
#----------------FLASK-------------------
#------------------------------------------

FROM python:3.9-slim-buster

RUN groupadd -g 999 python \
    && useradd -r -u 999 -g python python \
    && mkdir -p /usr/app \
    && python -m venv /usr/app/.venv \
    && chown -R python:python /usr/app 

ENV PATH="/usr/app/.venv/bin:$PATH"
ENV PIP_NO_CACHE_DIR=off

WORKDIR /usr/app

USER 999
COPY --chown=python:python requirements.txt requirements.txt
RUN pip install --upgrade pip && \
    pip install -r requirements.txt

COPY main.py main.py

EXPOSE 8080

CMD ["python", "main.py"]