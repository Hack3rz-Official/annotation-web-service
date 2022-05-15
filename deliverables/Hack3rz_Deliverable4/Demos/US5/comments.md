As part of US5 the way the prediction-service loads and stores the best model for the prediction was changed.
The first lines (L1-7) of the screenshot of the logs of the prediction service show that upon starting up,
the prediction service loads the best models from the database for each language. The timing output
shows that this only takes 18-20ms for all three models.

The two INFO:waitress log entries (L8-9) show that the prediction service is now using a production grade waitress server 
instead of the previous development one.

The log entries below the INFO:waitress entries (L10-14) show that the prediction service used the in-memory python3 model
to serve a prediction request for the python3 language. After the request is done, the last three log lines show that
the prediction service asynchronously checks if there is a better model available. In this case there was no better model
available and no model update was required.

Caveats / Known Issues:
- Currently there is a configuration bug in the training service that prevents us from demoing the actual downloading / updating of the model with the instances running in docker. However, the unit tests surrounding this functionality are passing, and we will demo the actual model update as soon as the configuration bug is fixed.

