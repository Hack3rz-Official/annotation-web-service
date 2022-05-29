<h1 align="center">
  Annotation Web Service
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
Annotation Web Service (AWS) is a syntax highlighting web service based on a [deep learning (DL) model](https://github.com/MEPalma/UZH-ASE-AnnotationWS-BaseLearner). The goal was to build an API that uses the DL model to provide syntax highlighting for Java, Kotlin and Python3. Furthermore, the incoming requests should be used to train the DL model and to further improve its accuracy. 

This `README.md` focuses on the technical aspects and the running and configuration of the services. For a more in-depth description of the functionalities, technologies and our development process please consult our [Wiki](https://github.com/Hack3rz-Official/annotation-web-service/wiki). The original motivation and requirements for this project can be found in the [project instructions](https://seal-uzh.notion.site/Annotation-WebService-b9621a3b1b5943cba21ede82d2fcbfe3) provided by the lecturers of the course.

## Microservices
The Annotation Web Service consists of the following microservices:


| Microservice                                                                                                     | Description                                                                                | Technology                                                              | Status                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                |
|------------------------------------------------------------------------------------------------------------------|--------------------------------------------------------------------------------------------|-------------------------------------------------------------------------|-------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------|
| [Annotation Service](https://github.com/Hack3rz-Official/annotation-web-service/tree/develop/annotation-service) | Handles the annotaion of code, i.e. lexing and highlighting.                               | Java with [Spring Boot](https://github.com/spring-projects/spring-boot) | [![SonarCloud Coverage](https://sonarcloud.io/api/project_badges/measure?project=annotation-service&metric=coverage&branch=develop)](https://sonarcloud.io/component_measures/metric/coverage/list?id=annotation-service) [![Code Smells](https://sonarcloud.io/api/project_badges/measure?project=annotation-service&metric=code_smells)](https://sonarcloud.io/summary/new_code?id=annotation-service) [![SonarCloud Bugs](https://sonarcloud.io/api/project_badges/measure?project=annotation-service&metric=bugs)](https://sonarcloud.io/component_measures/metric/reliability_rating/list?id=annotation-service) [![SonarCloud Vulnerabilities](https://sonarcloud.io/api/project_badges/measure?project=annotation-service&metric=vulnerabilities)](https://sonarcloud.io/component_measures/metric/security_rating/list?id=annotation-service) |
| [Prediction Service](https://github.com/Hack3rz-Official/annotation-web-service/tree/develop/prediction-service) | Handles the prediction of syntax highlighting.                                             | Python with [Flask](https://github.com/pallets/flask)                   | [![SonarCloud Coverage](https://sonarcloud.io/api/project_badges/measure?project=prediction-service&metric=coverage&branch=develop)](https://sonarcloud.io/component_measures/metric/coverage/list?id=prediction-service) [![Code Smells](https://sonarcloud.io/api/project_badges/measure?project=prediction-service&metric=code_smells)](https://sonarcloud.io/summary/new_code?id=prediction-service) [![SonarCloud Bugs](https://sonarcloud.io/api/project_badges/measure?project=prediction-service&metric=bugs)](https://sonarcloud.io/component_measures/metric/reliability_rating/list?id=prediction-service) [![SonarCloud Vulnerabilities](https://sonarcloud.io/api/project_badges/measure?project=prediction-service&metric=vulnerabilities)](https://sonarcloud.io/component_measures/metric/security_rating/list?id=prediction-service) |
| [Training Service](https://github.com/Hack3rz-Official/annotation-web-service/tree/develop/training-service)     | Handles the regularly conducted training and exchange of the underlying prediction models. | Python with [Flask](https://github.com/pallets/flask)                   | [![SonarCloud Coverage](https://sonarcloud.io/api/project_badges/measure?project=training-service&metric=coverage&branch=develop)](https://sonarcloud.io/component_measures/metric/coverage/list?id=training-service) [![Code Smells](https://sonarcloud.io/api/project_badges/measure?project=training-service&metric=code_smells)](https://sonarcloud.io/summary/new_code?id=training-service) [![SonarCloud Bugs](https://sonarcloud.io/api/project_badges/measure?project=training-service&metric=bugs)](https://sonarcloud.io/component_measures/metric/reliability_rating/list?id=training-service) [![SonarCloud Vulnerabilities](https://sonarcloud.io/api/project_badges/measure?project=training-service&metric=vulnerabilities)](https://sonarcloud.io/component_measures/metric/security_rating/list?id=training-service)                 |
| [Web API](https://github.com/Hack3rz-Official/annotation-web-service/tree/develop/web-api)                       | Acts as the primary entry point for the customers.                                         | JS/TS with [Nest.js](https://github.com/nestjs/nest)                    | [![SonarCloud Coverage](https://sonarcloud.io/api/project_badges/measure?project=web-api-service&metric=coverage&branch=develop)](https://sonarcloud.io/component_measures/metric/coverage/list?id=web-api-service) [![Code Smells](https://sonarcloud.io/api/project_badges/measure?project=web-api-service&metric=code_smells)](https://sonarcloud.io/summary/new_code?id=web-api-service) [![SonarCloud Bugs](https://sonarcloud.io/api/project_badges/measure?project=web-api-service&metric=bugs)](https://sonarcloud.io/component_measures/metric/reliability_rating/list?id=web-api-service) [![SonarCloud Vulnerabilities](https://sonarcloud.io/api/project_badges/measure?project=web-api-service&metric=vulnerabilities)](https://sonarcloud.io/component_measures/metric/security_rating/list?id=web-api-service)                         |

Every microservice is running in a Docker container. An extensive documentation of each microservice is provided in the [Wiki](https://github.com/Hack3rz-Official/annotation-web-service/wiki).

## Utils and Proof-of-Concepts
In addition to the microservices listed above, we have implemented a number of utils/helpers and a proof-of-concept of a demo-frontend that uses the API provided by the microservices.
These tools are intended for internal use only. Thus, they do not adhere to the same code quality standards as the microservices. Nevertheless, they demonstrate how the API can be used in various environments.

| **Tool**                                                                                               | **Description**                                                                                               | **Technology**                       |
|--------------------------------------------------------------------------------------------------------|---------------------------------------------------------------------------------------------------------------|--------------------------------------|
| [Demo Frontend](https://github.com/Hack3rz-Official/annotation-web-service/tree/develop/demo-frontend) | A single page webapp that demonstrates how the API could be used by a potential customer.                     | JS/TS with [Vue](https://vuejs.org/) |
| [Code Fetcher](https://github.com/Hack3rz-Official/annotation-web-service/tree/develop/code-fetcher)   | A command line tool to download source code from GitHub and send it to the API.                               | Python                               |
| [Load Tester](https://github.com/Hack3rz-Official/annotation-web-service/tree/develop/load-tester)     | A simple script to send a lot of concurrent requests to the API and analyze the performance under heavy load. | Javascript with [K6](https://k6.io/) |


## Configuration
The microservices rely on a number of environment variables for their configuration. The environment variables are defined in a `.env` file in the project root. This file is used within the `docker-compose.yml` to pass the configuration to the services. The following table displays an overview of the environment variables and their default values:
| **Variable Name**          | **Description**                                                            | **Example Value**                                                                               |
|----------------------------|----------------------------------------------------------------------------|-------------------------------------------------------------------------------------------------|
| `MONGO_USERNAME`           | The username used for the MongoDB.                                         | `hack3rz`                                                                                       |
| `MONGO_PASSWORD`           | The password used for the MongoDB.                                         | `palm_tree_poppin_out_the_powder_blue_sky`                                                      |
| `MONGO_DATABASE_NAME`      | The database name for the MongoDB.                                         | `aws`                                                                                           |
| `MONGO_DATABASE_TEST_NAME` | The test database name for the MongoDB.                                    | `aws_test`                                                                                      |
| `MONGO_PORT`               | The port on which the MongoDB runs.                                        | `27017`                                                                                         |
| `MONGO_HOST`               | The host for the MongoDB.                                                  | `mongodb`                                                                                       |
| `MONGO_AUTH_DATABASE`      | The database used in MongoDB for the authentication (holds default users). | `admin`                                                                                         |
| `DB_CONNECTION_STRING`     | The connection string for the MongoDB.                                     | `mongodb://hack3rz:palm_tree_poppin_out_the_powder_blue_sky@mongodb:27017/aws?authSource=admin` |
| `MODEL_NAME`               | The prefix used when storing a model locally on the disk.                  | `best`                                                                                          |
| `MIN_TRAINING_BATCH_SIZE`  | The minimum amount of annotations required before a training is started.   | `100`                                                                                           |
| `DEMO_FRONTEND_PORT`       | The port on which the demo frontend runs.                                  | `80`                                                                                            |
| `WEB_API_PORT`             | The port on which the web api runs.                                        | `8081`                                                                                          |
| `SWAGGER_UI_PORT`          | The port on which the Swagger UI runs.                                     | `8082`                                                                                          |
| `ANNOTATION_SERVICE_PORT`  | The port on which the annotation service runs.                             | `8083`                                                                                          |
| `PREDICTION_SERVICE_PORT`  | The port on which the prediction service runs.                             | `8084`                                                                                          |
| `TRAINING_SERVICE_PORT`    | The port on which the training service runs.                               | `8085`                                                                                          |
| `NGINX_PORT`          | The port on which the nginx load-balancer runs.                            | `4000`                                                                                          |


## Docker Containers
The following table contains a list of all docker containers that are part of the `docker-compose` setup and their respective images used. All the images prefixed with `richner` were developed as part of this project and are publicly available on [DockerHub](https://hub.docker.com/u/richner).
| **Name**      | **Description**                                                              | **Image**                                                                                |
|---------------|------------------------------------------------------------------------------|------------------------------------------------------------------------------------------|
| Demo Frontend | The single demo frontend.                                                    | [richner/demo-frontend:latest](https://hub.docker.com/r/richner/demo-frontend)           |
| Web API       | The web API that wraps all the other microservices.                          | [richner/web-api:latest](https://hub.docker.com/r/richner/web-api)                       |
| Swagger UI    | The swagger UI that holds the documentation for all services.                | [swaggerapi/swagger-ui](https://hub.docker.com/r/swaggerapi/swagger-ui)                  |
| Annotation    | The annotation service.                                                      | [richner/annotation-service:latest](https://hub.docker.com/r/richner/annotation-service) |
| Prediction    | The prediction service.                                                      | [richner/prediction-service:latest](https://hub.docker.com/r/richner/prediction-service) |
| Training      | The training service.                                                        | [richner/training-service:latest](https://hub.docker.com/r/richner/training-service)     |
| Nginx         | The NGINX load-balancer and reverse-proxy.                                   | [nginx:latest](https://hub.docker.com/_/nginx)                                           |
| MongoDB       | The MongoDB that is used by the annotation, prediction and training service. | [mongo:5.0.6](https://hub.docker.com/_/mongo)                                            |


## Run It Locally
Make sure that you use **Docker Compose V2** and activate it in your docker setup. Within Docker Desktop, go to "Settings" and toggle the “Use Docker Compose V2” option under the “General” tab. More information can be found [here](https://www.docker.com/blog/announcing-compose-v2-general-availability/). You can verify the setting by running:
```bash
$ docker-compose -v # should output v2.X.X
```

Use the following command to run all services using `docker-compose`:
```bash
$ docker-compose up --build --scale prediction=2 --scale annotation=2
```

Sometimes builds fail on machines with different processor architectures (e.g. on M1 MacBooks). In other cases the build might fail, because there are old versions of the docker containers stored. Use the following command for a clean new build:
```bash
$ docker-compose up -d --force-recreate --renew-anon-volumes --build --scale prediction=2 --scale annotation=2
```




### MongoDB
The MongoDB is launched as a separate Docker container. The credentials are stored within the environment of the other containers, so they can access it.
A folder `data` in the project root is mounted as a volume for the database. This folder will persist the data in the database even when the containers are reset. If you want to reset the database you can just delete the contents of this folder. The file `mongo-init.sh` is used to initialize the database with a new user and the credentials provided by the environment file.

#### Testing the connection
Make sure the mongodb container is running. Connect to the CLI of the container and use the following command to access the DB:
```bash
$ mongo --username "$MONGO_USERNAME" --password "$MONGO_PASSWORD"
```
Alternatively, you can use a GUI like [mongoDBCompass](https://www.mongodb.com/products/compass) to access the database.
### NGINX
To demonstrate the scaling and redundancy possibilities within the API [NGINX](https://www.nginx.com/) is used to act as a load-balancer and reverse-proxy for the annotation and prediction microservices. Consequently, the Web API interacts with NGINX which in turn forwards the requests to the respective microservices. This allows us to scale both the annotation and prediction services. The load is distributed using a round-robin method. The configuration for NGINX can be found in the `nginx.conf.template` file.

### Swagger REST API Documentation
All the endpoints of each microservice are documented using [Swagger](https://swagger.io/). Each microservice contains a `openapi.json` file that documents the endpoints using the [OpenApi](https://swagger.io/specification/) specification.
If the `docker-compose` is run there will be an additional swagger container running at `localhost:8082`.

## Azure Deployment
Currently, it's not possible to automate the deployment with GitHub Actions because our student subscription via UZH does not have the privilege to create a service account which would be required for automated deployments. However, there is a possibility to manually deploy the Docker containers to Azure. Please make sure your Azure account is owner of Azure's resource group called hack3rz and you have installed Azure CLI on your machine. Then use the following commands to deploy the containers:

1. Login to Azure with your credentials and setup context for Azure Container Instances (ACI):
```bash
$ az login
$ az account set --subscription 02b30768-05c8-4ad0-acc8-dda03818d4d6
$ az acr login --name hack3rzacr
$ docker login azure
```
2. Run the following shell script to deploy and redeploy the containers:
```bash
$ sh deploy-azure.sh
```

3. After a successful deployment you can check the status of the deployed containers at [Azure Portal](https://portal.azure.com/#@UZH.onmicrosoft.com/resource/subscriptions/d295f317-9001-4571-b6af-87b3296d016d/resourceGroups/hack3rz/overview). The public domain name is ```hack3rz-aws.switzerlandnorth.azurecontainer.io```. The demo is accessible via [http://hack3rz-aws.switzerlandnorth.azurecontainer.io](http://hack3rz-aws.switzerlandnorth.azurecontainer.io). A test request can be made with the following command:
```bash
$ curl -X 'POST' \
  'http://hack3rz-aws.switzerlandnorth.azurecontainer.io:8081/api/v1/highlight' \
  -H 'accept: */*' \
  -H 'Content-Type: application/json' \
  -d '{
  "code": "public static void main(String args[]){ System.out.println(\"testing\") }",
  "language": "java"
}'
```

The container configuration for the deployment on azure can be found in the file `docker-compose-azure.yml`.

### Deployment Caveats
The current deployment configuration found in `docker-compose-azure.yml` is a preliminary version. The following restrictions apply:
- CosmosDB instead of MongoDB is used
- Swagger UI is not deployed
- Nginx is not deployed
- Training Service cronjob does not work
- There is no model update
- Only a single instance of the prediction service is deployed
- Only a single instance of the annotation service is deployed

Consequently, the deployment only acts as a proof-of-concept and does not yet fully reflect the local docker setup.

## Demo
A demo is accessible via [http://hack3rz-aws.switzerlandnorth.azurecontainer.io](http://hack3rz-aws.switzerlandnorth.azurecontainer.io).

**Attention:** The restrictions / caveats mentioned above apply. Use `docker-compose` to test our service with its full functionality.

## Authors

This project has been built by team Hack3rz as part of the [Advanced Software Engineering](https://www.ifi.uzh.ch/en/seal/teaching/courses/ase.html) course at the [University of Zurich](https://www.uzh.ch/en.html) in the spring semester 2022:

- [Michael Ziörjen](https://github.com/miczed)
- [Sebastian Richner](https://github.com/SRichner)
- [Michael Blum](https://github.com/admi22)
- [Nicola Crimi](https://github.com/ncrimi)
- [Pascal Emmenegger](https://github.com/pemmenegger)

It is based on the following libraries:
- [UZH-ASE-AnnotationWS-FormalModel](https://github.com/MEPalma/UZH-ASE-AnnotationWS-FormalModel)
- [UZH-ASE-AnnotationWS-BaseLearner](https://github.com/MEPalma/UZH-ASE-AnnotationWS-BaseLearner)
