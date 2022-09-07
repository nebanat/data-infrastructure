FROM python:3.9.13-slim

RUN apt-get update \
    # dependencies for building Python packages
    && apt-get install -y build-essential \
    # psycopg2 dependencies
    && apt-get install -y libpq-dev \
    # install wget
    && apt-get install -y wget \
    # cleaning up unused files 
    && apt-get purge -y --autoremove -o APT::AutoRemove::RecommendsImportant=false \
    && rm -rf /var/lib/apt/lists/*
COPY ./requirements.txt requirements.txt
COPY ./main.py main.py

RUN pip install --upgrade pip && pip install -r requirements.txt

ENTRYPOINT [ "python" , "main.py" ]