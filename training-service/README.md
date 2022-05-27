# Training Service
[![sonarcloud workflow](https://github.com/Hack3rz-Official/annotation-web-service/actions/workflows/training-service-dockerhub.yml/badge.svg)](https://github.com/Hack3rz-Official/annotation-web-service/actions/workflows/training-service-sonarcloud.yml)
[![dockerhub workflow](https://github.com/Hack3rz-Official/annotation-web-service/actions/workflows/training-service-sonarcloud.yml/badge.svg)](https://github.com/Hack3rz-Official/annotation-web-service/actions/workflows/training-service-dockerhub.yml)
[![Quality Gate Status](https://sonarcloud.io/api/project_badges/measure?project=training-service&metric=alert_status)](https://sonarcloud.io/summary/new_code?id=training-service)
[![Coverage](https://sonarcloud.io/api/project_badges/measure?project=training-service&metric=coverage)](https://sonarcloud.io/summary/new_code?id=training-service)

A repository containing all source code for the training function which is based on the provided [UZH-ASE-AnnotationWS-BaseLearner](https://github.com/MEPalma/UZH-ASE-AnnotationWS-BaseLearner) repository.

A more detailed documentation can be found in the [Wiki for Training Service](https://github.com/Hack3rz-Official/annotation-web-service/wiki/Training-Service).

## Configuration
The service expects the following environment variables:
| **Variable Name**          | **Description**                                                            | **Example Value**                                                                               |
|----------------------------|----------------------------------------------------------------------------|-------------------------------------------------------------------------------------------------|
| `DB_CONNECTION_STRING`     | The connection string for the MongoDB.                                     | `mongodb://hack3rz:palm_tree_poppin_out_the_powder_blue_sky@mongodb:27017/aws?authSource=admin` |
| `MODEL_NAME`               | The prefix used when storing a model locally on the disk.                  | `best`                                                                                          |
| `MIN_TRAINING_BATCH_SIZE`  | The minimum amount of annotations required before a training is started.   | `100`                                                                                           |
| `TRAINING_SERVICE_PORT`    | The port on which the training service runs.                               | `8085`                                                                                          |
| `SWAGGER_UI_PORT`          | The port on which the Swagger UI runs.                                     | `8082`                                                                                          |


Please make sure that these environment variables are present when running the service. If you run it using the global `docker-compose` then they will automatically be passed to the service.

## Run Service Locally
Execute the following code from the `/training-service` directory:

```bash
# activate virtual environment and install dependencies
$ source venv.sh

# Set PYTHONPATH to current path
$ export PYTHONPATH="$PWD" # MacOS and Linux, for Windows see here: https://bic-berkeley.github.io/psych-214-fall-2016/using_pythonpath.html

# run flask api
$ python3 app.py
```

Finally, the service should be accessible via ```http://localhost:8085/api/v1/training```.

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

```bash
curl -X 'PUT' \
        'http://localhost:8085/api/v1/training' \
        -H 'accept: */*' \
        -H 'Content-Type: application/json' \
        -d '{ "model": "all" }'
```    

#### Sample Body
```json
{ "model": "all" }
```

#### Sample Response
```json
    {"message": "Models trained for java, python3, kotlin"}
```

For a more detailed documentation of the REST API please use SwaggerUI (available at `localhost:8082` when running `docker-compose`) or consult the `openapi.json` specification.