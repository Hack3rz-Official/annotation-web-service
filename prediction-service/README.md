# Prediction Service
[![sonarcloud workflow](https://github.com/Hack3rz-Official/annotation-web-service/actions/workflows/prediction-service-dockerhub.yml/badge.svg)](https://github.com/Hack3rz-Official/annotation-web-service/actions/workflows/prediction-service-sonarcloud.yml)
[![dockerhub workflow](https://github.com/Hack3rz-Official/annotation-web-service/actions/workflows/prediction-service-sonarcloud.yml/badge.svg)](https://github.com/Hack3rz-Official/annotation-web-service/actions/workflows/prediction-service-dockerhub.yml)
[![Quality Gate Status](https://sonarcloud.io/api/project_badges/measure?project=prediction-service&metric=alert_status)](https://sonarcloud.io/summary/new_code?id=prediction-service)
[![Coverage](https://sonarcloud.io/api/project_badges/measure?project=prediction-service&metric=coverage)](https://sonarcloud.io/summary/new_code?id=prediction-service)

A repository containing all source code for the predict functionality which is based on the provided [UZH-ASE-AnnotationWS-BaseLearner](https://github.com/MEPalma/UZH-ASE-AnnotationWS-BaseLearner) repository.

A more detailed documentation can be found in the [Wiki for Prediction Service](https://github.com/Hack3rz-Official/annotation-web-service/wiki/Prediction-Service).

## Configuration
The service expects the following environment variables:
| **Variable Name**         | **Description**                                                              | **Example Value**                                                                               |
|---------------------------|------------------------------------------------------------------------------|-------------------------------------------------------------------------------------------------|
| `DB_CONNECTION_STRING`    | The connection string for connecting to the MongoDb to load the best model.  | `mongodb://hack3rz:palm_tree_poppin_out_the_powder_blue_sky@mongodb:27017/aws?authSource=admin` |
| `PREDICTION_SERVICE_PORT` | The port on which the prediction service should run.                         | `8084`                                                                                          |

Please make sure that these environment variables are present when running the service. If you run it using the global `docker-compose` then they will automatically be passed to the service. 

## Run Service Locally
Execute the following code from the `/prediction-service` directory:

```bash
# activate virtual environment and install dependencies
$ source venv.sh

# Set PYTHONPATH to current path
$ export PYTHONPATH="$PWD" # MacOS and Linux, for Windows see here: https://bic-berkeley.github.io/psych-214-fall-2016/using_pythonpath.html

# run flask api
$ python3 app.py
```

Finally, the function should be accessible via `http://localhost:8084/api/v1/prediction`.

## Run Tests
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

The REST API to the predict service is described below.

### Predict

#### Request

`POST /api/v1/prediction`

```bash
    curl -X 'POST' \
        'http://localhost:8084/api/v1/prediction' \
        -H 'accept: application/json' \
        -H 'Content-Type: application/json' \
        -d '{
        "lang_name": "java",
        "tok_ids": [1,2,3,4,5,6,7,8,9,10]
    }'
```
#### Example Body:
```json
{
    "lang_name": "java",
    "tok_ids": [1,2,3,4,5,6,7,8,9,10]
}
```
#### Example Response
```json
  { "h_code_values": [10, 0, 3] }
```

For a more detailed documentation of the REST API please use SwaggerUI (available at `localhost:8082` when running `docker-compose`) or consult the `openapi.json` specification.    