US11 consists of the creation of a demo frontend for our web API that allows the user to interact with the API in an intuitive way.

We've built a simple javascript web application using the Vue framework that is interacting with our web api which in turn acts as a gateway for all the other microservices (such as annotation, prediction and training service).
The user has two options to highlight code:

We provide a number of demo files that can be loaded by clicking a button. Subsequently, each file is displayed without any highlighting.
Then the user can either highlight each file individually or highlight all the files at the same time. Clicking on an individual file
will open a dialog that shows the highlighted code and allows the user to make edits and send them to the API again.

Another option is to paste in the URL of a public GitHub repo. The demo application will fetch all the files and the user is then available to select how many files of each supported language should be loaded.

Caveats:
- Currently, the API throws an error if empty files are submitted.
- The highlighting shown in the video is not accurate, because the model used was not trained.