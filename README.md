# annotation-web-service
The repository containing all source code for the annotation web service.


| File/folder        | Description                                                                |
|--------------------|----------------------------------------------------------------------------|
| `deliverables`     | All deliverables for the respective submissions.                           |
| `function-lex`     | The source code of the cloud function that handles the lexing of the code. |
| `function-predict` | The source code of the cloud function that handles the prediction.         |
| `web-api`          | The web API that acts as the primary entry point for the customers.        |
| `.gitignore`       | Define what to ignore at commit time.                                      |
| `README.md`        | This README file.                                                          |



## Links
- [Azure Workspace](https://portal.azure.com/#@uzh.onmicrosoft.com/dashboard/arm/subscriptions/48c1a3cf-793a-4ca1-97e3-0e93cc815cb4/resourcegroups/hack3rz/providers/microsoft.portal/dashboards/39f628bf-8b8f-45c7-868e-968f8b24f196)




### Branching Policy

For this project, we will be using the popular Gitflow branching strategy. This enables us to develop features on different feature branches in parallel and merge them into the develop/main branch once a feature is completed and ready to be deployed on a development or production environment.

#### main

The main branch is always in a production-ready state and contains only code & features that can be released into production. Merges into main are part of the release and should only occur from release branches and only contain production-ready code. This allows us to setup a clean CI/CD workflow with an always up-to-date and working production environment deployed and running in the cloud

#### develop

The develop branch can at times be in an unstable state, but should be deployable to a development system for testing or inspections. This allows us to setup a clean CI/CD workflow with an always up-to-date and working development environment deployed and running in the cloud. We merge from feature branches into the develop branch using merge/pull requests. For special cases (exceptions) we may also commit directly to develop.

#### feature

Where possible, we create separate feature branches for each feature. This allows us to work on our applications in parallel and once ready, code reviews on specific code changes for each feature.


- Prefix: `feature/`
- Name: Issue/task identifier and short description
- e.g.: `feature/BACK-001_MyAwesomeFeature`

#### release

Once we have all our feature branches merged into the develop branch, we create a release branch off of develop. This starts the next release cycle and allows us to work on the next iteration and if needed make changes to the current release on the newly created release branch. Once the release branch is ready to be deployed to production, we merge it first into main and finally into develop.

- Prefix: `release/`
- Name: vX.X.X
- e.g.: `release/v1.2.3`

#### hotfix

The hotfix branch will be created if we encounter issues after a production release that need to be quickly fixed. They are created directly from the main branch and merged back into main and develop.

- Prefix: `hotfix/`
- Name: vX.X.X, the version to be fixed
- e.g.: `hotfix/v1.2.3`

