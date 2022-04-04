# Web API for Syntax Highlighting

## **Development Setup**

This app can be launched in a docker container (make sure you have docker and docker-compose installed)

```bash
docker-compose up dev
```
Alternatively you can launch the server without docker:
```bash
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
	"code": "class Simple { public static void main(String args[]){ int x = 5; }",
	"language": "java"
}
```
**Sample Response:**
```
// TODO: insert sample response here
```

