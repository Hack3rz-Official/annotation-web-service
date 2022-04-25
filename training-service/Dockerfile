# syntax=docker/dockerfile:1

FROM python:3.8.3-slim-buster

COPY requirements.txt requirements.txt
RUN pip3 install -r requirements.txt

COPY . .

# run our Flask app as a module
CMD [ "python3", "-m" , "flask", "run", "--host=0.0.0.0"]