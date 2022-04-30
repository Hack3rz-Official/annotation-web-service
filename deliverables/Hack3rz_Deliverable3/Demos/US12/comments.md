In US12 we wanted to provide a way for the owners of the API to train the model with a lot of files without
reyling on the demo-frontend or sending manual requests to the REST endpoints.

We implemented a small command line tool that fetches code files from GitHub, submits them to our API, so they can be used to
increase the accuracy of the model. The tool will download a specified amount of files from the most
starred repositories on GitHub and annotate them using our API.

Caveats:
- the tool is only intended for the developers of the API and thus has no public interface
- the lines of code per file is not calculated correctly at the moment
