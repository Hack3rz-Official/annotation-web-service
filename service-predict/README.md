# Service Predict
A repository containing all source code for the predict function which is based on the provided [UZH-ASE-AnnotationWS-BaseLearner](https://github.com/MEPalma/UZH-ASE-AnnotationWS-BaseLearner) repository.

## Running the function locally
Execute the following code from the `/service-predict` directory:

```bash
# activate virtual environment and install dependencies
$ source venv.sh

# Set PYTHONPATH to current path
$ export PYTHONPATH="$PWD" # MacOS and Linux, for Windows see here: https://bic-berkeley.github.io/psych-214-fall-2016/using_pythonpath.html

# run flask api
$ python3 app.py
```

Finally, the function should be running at ```http://127.0.0.1:5000/predict```. You can test if it works by a POST request with the following body:
```bash
# test via postman, send the following body with POST
{
    "lang_name":"java",
    "tok_ids":[34,22,45]
}
```

## Running the function locally via Docker

```bash
# build docker image
$ docker build --tag <YOUR_DOCKER_HUB_ID>/hack3rz-service-predict:v1.0.0 .

# run docker image
$ docker run -p 7071:5000 -it <YOUR_DOCKER_HUB_ID>/hack3rz-service-predict:v1.0.0
```

Finally, the function should be running at ```http://127.0.0.1:7071/predict```