This demo shows the implementation of US4 that consists of the updating of the model in case there is a better one available after a training. 
On a definable interval (e.g. 5 minutes) the training service will check if there are new code samples in the MongoDB database. 
If a certain threshold (currently 100 samples) is available for one of the three languages, the training will be started. If there is an
existing model in the database, the training service will fetch that model first and then train it on the newly available samples.

Before the actual training, the samples are split into training and validation sets that do not intersect. After the training,
the performance of the new model is evaluated on the validation set and if a higher accuracy was achieved, the new model is persisted
to the database. 

Whenever an instance of a prediction service is started, it will automatically fetch the best model available for each language and
use it for all the prediction requests.

In the next spring we'll address how to update the model as soon as a new one is available (instead of only when the prediction services are started up).