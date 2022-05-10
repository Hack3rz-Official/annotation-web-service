# syntax=docker/dockerfile:1

FROM python:3.8.3-slim-buster

COPY requirements.txt requirements.txt
RUN pip3 install -r requirements.txt

# install production server
RUN pip install waitress
COPY . .

CMD waitress-serve --port=${PREDICTION_SERVICE_PORT} --call app:create_app