# function-predict
A repository containing all source code for the predict function which is based on the provided [UZH-ASE-AnnotationWS-BaseLearner](https://github.com/MEPalma/UZH-ASE-AnnotationWS-BaseLearner) repository.

## Installation
In order to run and deploy the azure function from localhost, you need to first install Azure Functions Core Tools on your machine. Instructions can be found [here](https://docs.microsoft.com/en-us/azure/azure-functions/functions-run-local?tabs=v4%2Cmacos%2Ccsharp%2Cportal%2Cbash#install-the-azure-functions-core-tools).

## Running the function locally via Azure Functions Core Tools

```bash
# activate virtual environment and install dependencies
$ source venv.sh

# init your local function workers (if not already done)
$ func init

# run function
$ func start --python
```

Finally, the function should be running at ```http://localhost:7071/api/predict```

## Running the function locally via Docker

```bash
# build docker image
$ docker build --tag <YOUR_DOCKER_HUBB_ID>/hack3rz-function-predict:v1.0.0 .

# run docker image
$ docker run -p 7071:80 -it <YOUR_DOCKER_HUBB_ID>/hack3rz-function-predict:v1.0.0
```

Finally, the function should be running at ```http://localhost:7071/api/predict```
