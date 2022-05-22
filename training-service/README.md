# Training Service
A repository containing all source code for the training function which is based on the provided [UZH-ASE-AnnotationWS-BaseLearner](https://github.com/MEPalma/UZH-ASE-AnnotationWS-BaseLearner) repository.

## Run It Locally
Execute the following code from the `/training-service` directory:

```bash
# activate virtual environment and install dependencies
$ source venv.sh

# Set PYTHONPATH to current path
$ export PYTHONPATH="$PWD" # MacOS and Linux, for Windows see here: https://bic-berkeley.github.io/psych-214-fall-2016/using_pythonpath.html

# run flask api
$ python3 app.py
```

Finally, the function should be accessible via ```http://localhost:8085/api/v1/training```.

## Running Tests
First, make sure that MongoDB is also running locally by starting the Annotation Web Service with the docker-compose command as described in the project's main page. Then, execute the following code from the `/training-service` directory:

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

The REST API to the training service is described below.

### Training

The following request will manually trigger the training of models with available training data on the training database. By construction, the training procedure will be executed every 5 minutes anyways.

#### Request

`PUT /api/v1/training`

    curl -X 'PUT' \
        'http://localhost:8085/api/v1/training' \
        -H 'accept: */*' \
        -H 'Content-Type: application/json' \
        -d '{
        "model": "all"
    }'

#### Response

    {"message": "Not enough training data"}
