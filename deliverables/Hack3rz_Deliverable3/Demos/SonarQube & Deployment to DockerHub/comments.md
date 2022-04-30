In this sprint we've also added SonarQube and automatic deployment to DockerHub to our CI pipeline.
The whole pipeline runs using GitHub actions / workflows.

For each pull-request, GitHub actions will execute the tests for all the microservices. If the test-run was successful,
the code will be submitted to SonarQube that runs on SonarCloud to perform quality checks. The result of these checks
will be displayed directly in GitHub.

Furthermore, SonarQube provides us with a dashboard to monitor the overall quality of our code and displays metrics
such as test coverage and other insights such as potential code smells.

If the quality gate passes and if a branch is merged into the `main` branch, the deployment to dockerhub will be triggered automatically.
The images are available online here: https://hub.docker.com/u/richner

Caveats:
- Currently only a single version of each docker image for our microservices is available. 
- The test coverage is currently not sufficient for all of our microservices
- The quality gates still need to be adjusted for some microservices