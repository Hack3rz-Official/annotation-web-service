# Training Service
A repository containing all source code for the training function which is based on the provided [UZH-ASE-AnnotationWS-BaseLearner](https://github.com/MEPalma/UZH-ASE-AnnotationWS-BaseLearner) repository.

## REST API Documentation

The REST API to the training service is described below.

### Training

The following request will manually trigger the training of the models which available training data on the training database. By construction, the training procedure will be executed every 5 minutes anyways. 

#### Request

`GET /training/`

    curl -X GET http://localhost:6061/api/v1/training \
        -H "Content-Type: application/json"

#### Response

    200 OK

## Running the function locally
Execute the following code from the `/training-service` directory:

```bash
# activate virtual environment and install dependencies
$ source venv.sh

# Set PYTHONPATH to current path
$ export PYTHONPATH="$PWD" # MacOS and Linux, for Windows see here: https://bic-berkeley.github.io/psych-214-fall-2016/using_pythonpath.html

# run flask api
$ python3 app.py
```

Finally, the function should be running at ```http://127.0.0.1:8085/api/v1/training```. 

## Running the function locally via Docker

```bash
# build docker image
$ docker build --tag <YOUR_DOCKER_HUB_ID>/training-service:v1.0.0 .

# run docker image
$ docker run -p 8085:8085 -it <YOUR_DOCKER_HUB_ID>/training-service:v1.0.0
```

Finally, the function should be running at ```http://127.0.0.1:8085/api/v1/training```

## Running Tests
Run the following command to execute all tests within the `/test` folder. Make sure you activate the virtual environment and install the dependencies first.
```
python3 -m unittest discover test
```