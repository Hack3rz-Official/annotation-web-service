For the user story US11, we created a user interface to interact with our services.
In this sprint, we made several improvements to the demo frontend:

We added several tabs to group the different features together. The first tab includes the loading of files directly from a repository that can be specified. This behaves the same as in the previous version, except that we improved the way the number of files can be specified, as we replaced the slider with a number input field. Previously, we also showed the file size of each file, we found that this is hard to interpret and therefore, replaced it with the number of lines of code.

In the second tab that we added this spring, the user can load benchmark files for each language and select the size of the files (choose between small, medium, and large). This is useful to make multiple requests and then compare the response times with each other (as opposed to various file sizes, which can be done when loading an external repository from the first tab). 

We also added a statistics tab, where all the highlight requests for the files can be visualized and shown in a chart. This enables the user to compare the influence of the different languages and lines of code on the response times. Below the chart, there is also a table with the number of files, computed average and median times for each language.

The last tab contains the settings, where the user can change the number of concurrent requests that are made from the demo client/frontend to the web api. Finally, we added a setting to disable the previews for the file, as we found out that with dozens of files opened/highlighted in the browser, the browser uses a lot of resources.

We will further improve the documentation of our services and the demo in the upcoming weeks.

Caveats:
- Currently, we don't show the concrete number of files to be highlighted in the button
