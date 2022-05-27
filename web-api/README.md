# Web API for Syntax Highlighting
[![sonarcloud workflow](https://github.com/Hack3rz-Official/annotation-web-service/actions/workflows/web-api-service-dockerhub.yml/badge.svg)](https://github.com/Hack3rz-Official/annotation-web-service/actions/workflows/web-api-service-sonarcloud.yml)
[![dockerhub workflow](https://github.com/Hack3rz-Official/annotation-web-service/actions/workflows/web-api-service-sonarcloud.yml/badge.svg)](https://github.com/Hack3rz-Official/annotation-web-service/actions/workflows/web-api-service-dockerhub.yml)
[![Quality Gate Status](https://sonarcloud.io/api/project_badges/measure?project=web-api-service&metric=alert_status)](https://sonarcloud.io/summary/new_code?id=web-api-service)
[![Coverage](https://sonarcloud.io/api/project_badges/measure?project=web-api-service&metric=coverage)](https://sonarcloud.io/summary/new_code?id=web-api-service)

The Web API service acts as a gateway and is the central entry point of the Annotation Web Service through which each user request is processed.
It communicates first with the Annotation Service and consecutively with the Prediction Service before it returns a styled HTML response to the client.

A more detailed documentation can be found in [the wiki](https://github.com/Hack3rz-Official/annotation-web-service/wiki/Web-API).

## Configuration
The service expects the following environment variables:

| **Variable Name** | **Description**                     | **Example Value**                     |
|-------------------|-------------------------------------|---------------------------------------|
| `LEX_URL`         | The URL of the lexing service.      | `http://nginx:4000/api/v1/annotation` |
| `PREDICTION_URL`  | The URL of the prediction service.  | `http://nginx:4000/api/v1/prediction` |
| `WEB_API_PORT`    | The port on which the web api runs. | `8081`                                |

You can provide these environment variables using the `.env` file in the root of this directory. If you run the service using the global `docker-compose` then they will be passed automatically.


## Run Service Locally
Install the dependencies first, we use [npm](https://www.npmjs.com/) for this project.
```bash
# inside /web-api:
$ npm install
```

And then start the service:
```bash
$ npm run start
# or start in watch mode (with live-reload):
$ npm run start:dev
```
The service should now be running on port 8081 and should be available at `http://localhost:8081/`.

**Note:** Because this service depends on other microservices from the AnnotationWebService project, we recommended executing the docker-compose file in the project root to prevent dependency issues.

## Running Tests
Run the following command to execute the web service's tests.
```bash
$ yarn test
# or with coverage:
$ yarn test:cov
```


## **REST API Documentation**

| Method | Endpoint   | Content Type     |
|:-------|:-----------|:-----------------|
| POST   | /highlight | application/json |

#### Request

`POST /highlight`
```bash
$ curl -X 'POST' \
    'http://localhost:8081/api/v1/highlight' \
    -H 'accept: */*' \
    -H 'Content-Type: application/json' \
    -d '{
        "language": "java",
        "code": "public class Test { public void test() { System.out.println(\"Hello World\"); } }"
    }'
```
**Sample Body:**
```json
{
  "language": "java"
  "code": "public class Test { public void test() { System.out.println('Hello World'); } }",
}
```
**Sample Response:**
```html
<!DOCTYPE html>
<html>
<style>
  .ANY {
    color: black;
    font-weight: normal;
    font-style: normal;
  }
  .KEYWORD {
    color: blue;
    font-weight: bold;
    font-style: normal;
  }
  .LITERAL {
    color: lightskyblue;
    font-weight: bold;
    font-style: normal;
  }
  .CHAR_STRING_LITERAL {
    color: darkgoldenrod;
    font-weight: normal;
    font-style: normal;
  }
  .COMMENT {
    color: grey;
    font-weight: normal;
    font-style: italic;
  }
  .CLASS_DECLARATOR {
    color: crimson;
    font-weight: bold;
    font-style: normal;
  }
  .FUNCTION_DECLARATOR {
    color: fuchsia;
    font-weight: bold;
    font-style: normal;
  }
  .VARIABLE_DECLARATOR {
    color: purple;
    font-weight: bold;
    font-style: normal;
  }
  .TYPE_IDENTIFIER {
    color: darkgreen;
    font-weight: bold;
    font-style: normal;
  }
  .FUNCTION_IDENTIFIER {
    color: dodgerblue;
    font-weight: normal;
    font-style: normal;
  }
  .FIELD_IDENTIFIER {
    color: coral;
    font-weight: normal;
    font-style: normal;
  }
  .ANNOTATION_DECLARATOR {
    color: lightslategray;
    font-weight: lighter;
    font-style: italic;
  }
</style>
<pre>
  <code>
    <span class='ANNOTATION_DECLARATOR'>public</span> <span class='FUNCTION_IDENTIFIER'>static</span> <span class='TYPE_IDENTIFIER'>void</span> <span class='KEYWORD'>main</span><span class='FIELD_IDENTIFIER'>(</span><span class='FIELD_IDENTIFIER'>String</span><span class='CLASS_DECLARATOR'>[</span><span class='FIELD_IDENTIFIER'>]</span> <span class='FIELD_IDENTIFIER'>args</span><span class='CHAR_STRING_LITERAL'>)</span> <span class='CHAR_STRING_LITERAL'>{</span><span class='FUNCTION_DECLARATOR'>}</span>
  </code>
</pre>
</html>
```

For a more detailed documentation of the REST API please use SwaggerUI (available at `localhost:8082` when running `docker-compose`) or consult the `openapi.json` specification.

