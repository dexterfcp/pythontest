# 
FROM python:3.9

WORKDIR /code

COPY ./requirements.txt /code/requirements.txt
COPY ./app /code/app
COPY ./.env /code/.env

RUN pip install --no-cache-dir --upgrade -r /code/requirements.txt


