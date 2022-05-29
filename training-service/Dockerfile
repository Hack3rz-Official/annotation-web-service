# syntax=docker/dockerfile:1

FROM python:3.8.3-slim

# Install required dependencies that are not available in the slimmed down linux container
# referenced above
RUN apt-get update && apt-get install -y --no-install-recommends gcc python-dev

# the --no-install-recommends helps limit some of the install so that you can be more explicit about what gets installed

COPY requirements.txt requirements.txt
RUN export PIP_DEFAULT_TIMEOUT=100
RUN pip3 install -r requirements.txt

# purge build dependencies
RUN apt-get purge -y --auto-remove gcc python-dev

COPY . .

CMD python3 -m flask run --host=0.0.0.0 --port=${TRAINING_SERVICE_PORT}