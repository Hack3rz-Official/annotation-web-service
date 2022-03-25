# function-predict
A repository containing all source code for the predict function which is based on the provided [UZH-ASE-AnnotationWS-BaseLearner](https://github.com/MEPalma/UZH-ASE-AnnotationWS-BaseLearner) repository.

## Installation
In order to run and deploy the azure function from localhost, you need to first install Azure Functions Core Tools on your machine. Instructions can be found [here](https://docs.microsoft.com/en-us/azure/azure-functions/functions-run-local?tabs=v4%2Cmacos%2Ccsharp%2Cportal%2Cbash#install-the-azure-functions-core-tools).

## Running the function

```bash
# activate virtual environment and install dependencies
$ source venv.sh

# init your local function workers
$ func init

# run function
$ func start --python
```

Finally, the function should be running at ```http://localhost:7071/api/predict```

## Deploying the function
Before deploying the function make sure to uncomment the deployment dependencies of torch in requirements.txt and comment its local dependencies.