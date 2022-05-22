# Web API for Syntax Highlighting

The Web API service acts as a gateway and is the central entry point of the Annotation Web Service through which each user request is processed.
It communicates first with the Annotation Service and consecutively with the Prediction Service before it returns a styled HTML response to the client.

A more detailed documentation can be found in [the wiki](https://github.com/Hack3rz-Official/annotation-web-service/wiki/Web-API).

## **REST API Documentation**

| Method | Endpoint   | Content Type     |
|:-------|:-----------|:-----------------|
| POST   | /highlight | application/json |

#### Request

`POST /highlight`
```
curl -X 'POST' \
    'http://localhost:8081/api/v1/highlight' \
    -H 'accept: */*' \
    -H 'Content-Type: application/json' \
    -d '{
        "language": "java",
        "code": "public class Test { public void test() { System.out.println(\"Hello World\"); } }"
    }'
```
**Sample Body:**
```
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

## Running the function locally via Docker
Because this service depends on other microservices from the AnnotationWebService project, we recommended to execute the docker-compose file in the project root to prevent dependency issues:

```bash
# inside the project's root:
docker-compose up
```
Alternatively you can launch the server without docker, as described in the following section.

## Running the service locally
Install the dependencies first, we use npm for this project.
```bash
# inside /web-api:
npm install
```

And then start the service:
```bash
npm run start
# or start in watch mode (with live-reload):
npm run start:dev
```
The service should now be running on port 8081 and should be available at `http://localhost:8081/`.

## Running Tests
Run the following command to execute the web service's tests.
```bash
yarn test
# or with coverage:
yarn test:cov
```