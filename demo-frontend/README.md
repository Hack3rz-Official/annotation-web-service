# Demo Frontend

This demo was created to show the capabilities of our Annotation Service in action. It covers the following features:
- Load source code files from existing Github repositories
- Load Benchmark files for reproducible performance testing
- Perform Highlighting requests for individual files or in bulk
- Edit source files to see how the API responds to semantically invalid code snippets
- Change language of files, including invalid languages
- Analyze response times with visualized Statistics
- Simulate up to 10 concurrent requests


## Architecture
This is a Vue 3 SPA project leveraging the Tailwind styles library in combination with DaisyUI components. 

## Setup

This demo is accessible after launching the project-wide docker-compose file at port :80

```bash
# inside project root /:
docker-compose up
```
You can also launch this app without docker for development:
```bash
# inside /demo-frontend:
npm install
npm run dev
```
<br>

![Architecture](./aws_demo_frontend.png)