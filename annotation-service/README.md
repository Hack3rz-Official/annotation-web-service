# Annotation Service


[![sonarcloud workflow](https://github.com/Hack3rz-Official/annotation-web-service/actions/workflows/annotation-service-dockerhub.yml/badge.svg)](https://github.com/Hack3rz-Official/annotation-web-service/actions/workflows/annotation-service-sonarcloud.yml)
[![dockerhub workflow](https://github.com/Hack3rz-Official/annotation-web-service/actions/workflows/annotation-service-sonarcloud.yml/badge.svg)](https://github.com/Hack3rz-Official/annotation-web-service/actions/workflows/annotation-service-dockerhub.yml)
[![Quality Gate Status](https://sonarcloud.io/api/project_badges/measure?project=annotation-service&metric=alert_status)](https://sonarcloud.io/summary/new_code?id=annotation-service)
[![Coverage](https://sonarcloud.io/api/project_badges/measure?project=annotation-service&metric=coverage)](https://sonarcloud.io/summary/new_code?id=annotation-service)

A repository containing all source code for the annotation functionality which is based on the provided [UZH-ASE-AnnotationWS-FormalModel](https://github.com/MEPalma/UZH-ASE-AnnotationWS-FormalModel) repository.

A more detailed documentation can be found in the [Wiki for Annotation Service](https://github.com/Hack3rz-Official/annotation-web-service/wiki/Annotation-Service).

## Configuration
The service expects the following environment variables:
| **Variable Name**             | **Description**                                             | **Example Value**                                                                                 |
|-------------------------------|-------------------------------------------------------------|---------------------------------------------------------------------------------------------------|
| `ANNOTATION_SERVICE_PORT`     | The port on which the server for this service will run.     | `8083`                                                                                            |
| `DB_CONNECTION_STRING`        | The connection string used to connect to the MongoDB.       | `mongodb://hack3rz:palm_tree_poppin_out_the_powder_blue_sky@127.0.0.1:27017/aws?authSource=admin` |

These variables can be placed in the `.env` file in this directory for local development. 

## Run Service Locally
Execute the following code from the `/annotation-service` directory:

```bash
# build jar file
$ ./gradlew build

# run generated jar file
$ java -jar "build/libs/annotation-service-0.0.1-SNAPSHOT.jar"
```

Please also make sure that a MongoDB instance is running and configured using the environment variable. If you run this service as part of the global docker-compose for all the services then the database is run and configured automatically.

## Run Tests
```bash
$ ./gradlew clean test --info
```
- use `clean` if you want to re-run tests that have already passed since the last change
- use `--info` if you want to see test output

Finally, the function should be accessible via `http://localhost:8083/api/api/v1/annotation`.
For the tests, the service will automatically configure and run an in-memory MongoDB.

## **REST API Documentation**

| Method | Endpoint           | Content Type     |
|:-------|:-------------------|:-----------------|
| POST   | /api/v1/annotation | application/json |

#### Request

`POST /api/v1/annotation`
```bash
$ curl -X 'POST' \
    'http://localhost:8083/api/v1/annotation' \
    -H 'accept: */*' \
    -H 'Content-Type: application/json' \
    -d '{
        "language": "JAVA",
        "code": "public class Test { public void test() { System.out.println(\"Hello World\"); } }"
    }'
```
**Sample Body:**
```json
{
  "language": "JAVA",
  "code": "public class Test { public void test() { System.out.println('Hello World'); } }"
}
```
**Sample Response:**
```json
[
  {
    "startIndex": 0,
    "endIndex": 5,
    "tokenId": 35
  },
  {
    "startIndex": 7,
    "endIndex": 11,
    "tokenId": 9
  }
  // rest of response was omitted for readability purposes
]
```
For a more detailed documentation of the REST API please use SwaggerUI (available at `localhost:8082` when running `docker-compose`) or consult the `openapi.json` specification.


## Documentation & Source Code
The source code was documented using the [Javadoc](https://www.oracle.com/technical-resources/articles/java/javadoc-tool.html#styleguide) style guide. Furthermore, the source code makes use of [Lombok](https://projectlombok.org/) annotations to facilitate the implementation of boilerplate code (Getters, Setters, etc.). 