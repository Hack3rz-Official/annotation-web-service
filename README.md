<h1 align="center">
  Annotation WebService
  <br>
</h1>
<p align="center">
  <!--<a href="https://github.com/Hack3rz-Official/annotation-web-service/actions">
    <img src="https://github.com/Hack3rz-Official/annotation-web-service/workflows/Deploy%20Project/badge.svg">
  </a>-->
  <a href="https://sonarcloud.io/organizations/hack3rz-official/projects">
    <img width="150" src="https://sonarcloud.io/images/project_badges/sonarcloud-white.svg">
  </a>
</p>

## Introduction
A syntax highlighting web service based on AI. Please read the [project instructions](https://seal-uzh.notion.site/Annotation-WebService-b9621a3b1b5943cba21ede82d2fcbfe3) for more details about all functionalities.

## Microservices
Under the hood, the Annotation WebService consists of the following independent microservices:


| Microservice                                                                                                     | Description                                                                                | Technology                                                              | Status                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                |
|------------------------------------------------------------------------------------------------------------------|--------------------------------------------------------------------------------------------|-------------------------------------------------------------------------|-------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------|
| [Annotation Service](https://github.com/Hack3rz-Official/annotation-web-service/tree/develop/annotation-service) | Handles the annotaion of code, i.e. lexing and highlighting.                               | Java with [Spring Boot](https://github.com/spring-projects/spring-boot) | [![SonarCloud Coverage](https://sonarcloud.io/api/project_badges/measure?project=annotation-service&metric=coverage&branch=develop)](https://sonarcloud.io/component_measures/metric/coverage/list?id=annotation-service) [![Code Smells](https://sonarcloud.io/api/project_badges/measure?project=annotation-service&metric=code_smells)](https://sonarcloud.io/summary/new_code?id=annotation-service) [![SonarCloud Bugs](https://sonarcloud.io/api/project_badges/measure?project=annotation-service&metric=bugs)](https://sonarcloud.io/component_measures/metric/reliability_rating/list?id=annotation-service) [![SonarCloud Vulnerabilities](https://sonarcloud.io/api/project_badges/measure?project=annotation-service&metric=vulnerabilities)](https://sonarcloud.io/component_measures/metric/security_rating/list?id=annotation-service) |
| [Prediction Service](https://github.com/Hack3rz-Official/annotation-web-service/tree/develop/prediction-service) | Handles the prediction of syntax highlighting.                                             | Python with [Flask](https://github.com/pallets/flask)                   | [![SonarCloud Coverage](https://sonarcloud.io/api/project_badges/measure?project=prediction-service&metric=coverage&branch=develop)](https://sonarcloud.io/component_measures/metric/coverage/list?id=prediction-service) [![Code Smells](https://sonarcloud.io/api/project_badges/measure?project=prediction-service&metric=code_smells)](https://sonarcloud.io/summary/new_code?id=prediction-service) [![SonarCloud Bugs](https://sonarcloud.io/api/project_badges/measure?project=prediction-service&metric=bugs)](https://sonarcloud.io/component_measures/metric/reliability_rating/list?id=prediction-service) [![SonarCloud Vulnerabilities](https://sonarcloud.io/api/project_badges/measure?project=prediction-service&metric=vulnerabilities)](https://sonarcloud.io/component_measures/metric/security_rating/list?id=prediction-service) |
| [Training Service](https://github.com/Hack3rz-Official/annotation-web-service/tree/develop/training-service)     | Handles the regularly conducted training and exchange of the underlying prediction models. | Python with [Flask](https://github.com/pallets/flask)                   | [![SonarCloud Coverage](https://sonarcloud.io/api/project_badges/measure?project=training-service&metric=coverage&branch=develop)](https://sonarcloud.io/component_measures/metric/coverage/list?id=training-service) [![Code Smells](https://sonarcloud.io/api/project_badges/measure?project=training-service&metric=code_smells)](https://sonarcloud.io/summary/new_code?id=training-service) [![SonarCloud Bugs](https://sonarcloud.io/api/project_badges/measure?project=training-service&metric=bugs)](https://sonarcloud.io/component_measures/metric/reliability_rating/list?id=training-service) [![SonarCloud Vulnerabilities](https://sonarcloud.io/api/project_badges/measure?project=training-service&metric=vulnerabilities)](https://sonarcloud.io/component_measures/metric/security_rating/list?id=training-service)                 |
| [Web API](https://github.com/Hack3rz-Official/annotation-web-service/tree/develop/web-api)                       | Acts as the primary entry point for the customers.                                         | JS/TS with [Nest.js](https://github.com/nestjs/nest)                    | [![SonarCloud Coverage](https://sonarcloud.io/api/project_badges/measure?project=web-api-service&metric=coverage&branch=develop)](https://sonarcloud.io/component_measures/metric/coverage/list?id=web-api-service) [![Code Smells](https://sonarcloud.io/api/project_badges/measure?project=web-api-service&metric=code_smells)](https://sonarcloud.io/summary/new_code?id=web-api-service) [![SonarCloud Bugs](https://sonarcloud.io/api/project_badges/measure?project=web-api-service&metric=bugs)](https://sonarcloud.io/component_measures/metric/reliability_rating/list?id=web-api-service) [![SonarCloud Vulnerabilities](https://sonarcloud.io/api/project_badges/measure?project=web-api-service&metric=vulnerabilities)](https://sonarcloud.io/component_measures/metric/security_rating/list?id=web-api-service)                         |

Every microservice is running in a Docker container. An extensive documentation of each microservice is provided in the [Wiki](https://github.com/Hack3rz-Official/annotation-web-service/wiki).


## How it works
The following illustration depicts the general architecture of our Annotation WebService. It consists of two main flows namely the Syntax Highlighting Flow which is colored in red and the Training Flow colored in blue.

![Architecture](./architecture.png)

### Syntax Highlighting Flow
The red Syntax Highlighting Flow will be executed after a user request and handles the syntax highlighting of code from the user request as input to the highlighted code as output:
1. A user is requesting syntax highlighting with source code and its corresponding programming language.
2. The source code is sent to the *Annotation Service* where it will be lexed and highlighted. The *Annotation Service* returns the lexed code to the *Web API* and stores the whole request in the database which will be later used for the Training Flow.
3. After having received the lexed code from the *Annotataion Service* the *Web API* redirects it to the *Prediction Service* where first the current model needs to be loaded from the database.
4. After having loaded the best syntax highlighting model from the database, the *Prediction Service* will return the predicted `h_code_values` to the *Web API*.
5. Finally, the *Web API* transforms the `h_code_values` and the corresponding source code to a styled HTML which will be sent to the user as highlighted code.

### Training Flow
The blue Training Flow will automatically be triggered every 5 minutes and handles the training of the syntax highlighting models. The following steps will only be executed if there is enough training data on the database:
1. The *Training Service* loads the currently best model, the training dataset and validation dataset from the database. Then, the currently best model will be finetuned on the training data.
2. If the fine-tuned model does have a better accuracy on the same validation dataset as the currenntly best model, the *Training Service* will store the finetuned model as the new best model in the database and flag the training and validation dataset as used which will be considered during the next Training Flow. Otherwise, nothing will happen and the Training Flow will terminate.

## Demo
A demo is accessible via [http://hack3rz-aws.switzerlandnorth.azurecontainer.io:8080](http://hack3rz-aws.switzerlandnorth.azurecontainer.io:8080).

## Run It Locally
Use the following command to run all services using docker-compose:
```
docker-compose up --build --scale annotation=2
```
To test the load-balancing and scaling make sure to scale some services:
```
docker-compose up --build --scale prediction=2 --scale annotation=2
```

Sometimes builds fail on machines with different processor architectures (e.g. on M1 MacBooks). In other cases the build might fail, because there are old versions of the docker containers stored. Use the following command for a clean new build:
```
docker-compose up -d --force-recreate --renew-anon-volumes --build --scale prediction=2 --scale annotation=2
```

### MongoDB
The MongoDB is launched as a separate Docker container. The credentials are stored within the environment of the other containers, so they can access it.
A folder `data` in the project root is mounted as a volume for the database. 
When the container is launched initially a new database and user are created with the credentials from the environment file.

#### Testing the connection
Make sure the mongodb container is running. Connect to the CLI of the container and use the following command to access the DB:
`mongo --username "$MONGO_USERNAME" --password "$MONGO_PASSWORD"`

## Azure Deployment
Currently, it's not possible to automate the deployment with GitHub Actions because our student subscription via UZH doesn't have the privilege to create a service account which would be required for automated deployments. However, there is a possibility to manually deploy the Docker containers to Azure. Please make sure your Azure account is owner of Azure's resource group called hack3rz and you have installed Azure CLI on your machine. Then use the following commands to deploy the containers:

1. Login to Azure with your credentials and setup context for Azure Container Instances (ACI):
```bash
az login
az acr login --name hack3rzacr
docker login azure
docker context create aci hack3rzacicontext # run only once
```
2. Run the following shell script to deploy and redeploy the containers:
```
sh deploy-azure.sh
```

3. After a successful deployment you can check the status of the deployed containers at [Azure Portal](https://portal.azure.com/#@UZH.onmicrosoft.com/resource/subscriptions/d295f317-9001-4571-b6af-87b3296d016d/resourceGroups/hack3rz/overview). The public domain name is ```hack3rz-aws.switzerlandnorth.azurecontainer.io```. The demo is accessible via [http://hack3rz-aws.switzerlandnorth.azurecontainer.io:8080](http://hack3rz-aws.switzerlandnorth.azurecontainer.io:8080). A test request can be made with the following command:
```
curl -X 'POST' \
  'http://hack3rz-aws.switzerlandnorth.azurecontainer.io:8081/api/v1/highlight' \
  -H 'accept: */*' \
  -H 'Content-Type: application/json' \
  -d '{
  "code": "public static void main(String args[]){ System.out.println(\"testing\") }",
  "language": "java"
}'
```
### Authors

This project has been built by team Hack3rz:

- [Michael Ziörjen](https://github.com/miczed)
- [Sebastian Richner](https://github.com/SRichner)
- [Michael Blum](https://github.com/admi22)
- [Nicola Crimi](https://github.com/ncrimi)
- [Pascal Emmenegger](https://github.com/pemmenegger)

It is based on the following libraries:
- [UZH-ASE-AnnotationWS-FormalModel](https://github.com/MEPalma/UZH-ASE-AnnotationWS-FormalModel)
- [UZH-ASE-AnnotationWS-BaseLearner](https://github.com/MEPalma/UZH-ASE-AnnotationWS-BaseLearner)
