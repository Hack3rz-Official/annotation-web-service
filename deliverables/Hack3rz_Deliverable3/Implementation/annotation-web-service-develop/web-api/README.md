# Web API for Syntax Highlighting

## **Development Setup**

Because this service depends on other microservices from the AnnotationWebService project, we recommended to execute the docker-compose file in the project root to prevent dependency issues:

```bash
# inside project root /:
docker-compose up
```
Alternatively you can launch the server without docker:
```bash
# inside /web-api:
npm install
npm run start:dev
```
<br>

## **API Documentation**



| Method | Endpoint   | Content Type
|:-------|:-----------|:------------------|
| POST   | /highlight | application/json
**Sample Body:** 
```
{
	"code": "public static void main(String[] args) {}",
	"language": "java"
}
```
**Sample Response:**
```
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
    <pre><code><span class='ANNOTATION_DECLARATOR'>public</span> <span class='FUNCTION_IDENTIFIER'>static</span> <span class='TYPE_IDENTIFIER'>void</span> <span class='KEYWORD'>main</span><span class='FIELD_IDENTIFIER'>(</span><span class='FIELD_IDENTIFIER'>String</span><span class='CLASS_DECLARATOR'>[</span><span class='FIELD_IDENTIFIER'>]</span> <span class='FIELD_IDENTIFIER'>args</span><span class='CHAR_STRING_LITERAL'>)</span> <span class='CHAR_STRING_LITERAL'>{</span><span class='FUNCTION_DECLARATOR'>}</span>
    </pre>
    </code>
    </html>
    
```
