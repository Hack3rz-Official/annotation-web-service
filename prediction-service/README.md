# Predcition Service
A repository containing all source code for the predict functionality which is based on the provided [UZH-ASE-AnnotationWS-BaseLearner](https://github.com/MEPalma/UZH-ASE-AnnotationWS-BaseLearner) repository.

## Run It Locally
Execute the following code from the `/prediction-service` directory:

```bash
# activate virtual environment and install dependencies
$ source venv.sh

# Set PYTHONPATH to current path
$ export PYTHONPATH="$PWD" # MacOS and Linux, for Windows see here: https://bic-berkeley.github.io/psych-214-fall-2016/using_pythonpath.html

# run flask api
$ python3 app.py
```

Finally, the function should be accessible via ```http://localhost:8084/api/v1/prediction```.

## Running Tests
First, make sure that MongoDB is also running locally by starting the Annotation Web Service with the docker-compose command as described in the project's main page. Then, execute the following code from the `/prediction-service` directory:

```bash
# activate virtual environment and install dependencies
$ source venv.sh

# Set PYTHONPATH to current path
$ export PYTHONPATH="$PWD" # MacOS and Linux, for Windows see here: https://bic-berkeley.github.io/psych-214-fall-2016/using_pythonpath.html

# change to test directory
$ cd test

# Run all tests
$ python3 -m unittest discover

# Run specific test
$ python3 -m unittest <name-of-file.py>
```

## REST API Documentation

The REST API to the service predict is described below.

### Predict

#### Request

`POST /api/v1/prediction`

    curl -X 'POST' \
        'http://localhost:8084/api/v1/prediction' \
        -H 'accept: application/json' \
        -H 'Content-Type: application/json' \
        -d '{
        "lang_name": "java",
        "tok_ids": [
            1,
            2,
            3,
            4,
            5,
            6,
            7,
            8,
            9,
            10
        ]
    }'

#### Response

    {"h_code_values": [10, 0, 3]}