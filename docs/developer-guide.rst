.. ===============LICENSE_START=======================================================
.. Acumos CC-BY-4.0
.. ===================================================================================
.. Copyright (C) 2017-2018 AT&T Intellectual Property. All rights reserved.
.. ===================================================================================
.. This Acumos documentation file is distributed by AT&T
.. under the Creative Commons Attribution 4.0 International License (the "License");
.. you may not use this file except in compliance with the License.
.. You may obtain a copy of the License at
..
..      http://creativecommons.org/licenses/by/4.0
..
.. This file is distributed on an "AS IS" BASIS,
.. WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
.. See the License for the specific language governing permissions and
.. limitations under the License.
.. ===============LICENSE_END=========================================================

======================================================
Acumos RDS (R Data) Predictor Python Developer Guide
======================================================

This RDS predictor is used for running predictions on R object files.   These models are generally saved via the R command saveRDS.  This service also requires having R installed in its environment and RScript to be available on the system path.  This service has a dependency on model-manager for downloading models.

This service has a dependency to model-management to download the models.  AsyncPredictions and status methods are yet to be implemented in this version.

Sample model creation
=====================
.. code:: bash

    $ library(ggplot2)
    $ library(caret)
    $ library(leaps)
    $ library(factoextra)
    $ library(pmml)
    $ 
    $ #These are required for running in RDS Predictor
    $ #library RTextTools
    $ #library tm
    $ #library SparseM
    $ 
    $ 
    $ #Load the data
    $ data(mtcars)
    $ 
    $ #Format the data the way we want them (Lable them)
    $ mtcars$gear <- factor(mtcars$gear,levels=c(3,4,5),
     $                      labels=c("3gears","4gears","5gears"))
    $ mtcars$am <- factor(mtcars$am,levels=c(0,1),
    $                     labels=c("Automatic","Manual"))
    $ mtcars$cyl <- factor(mtcars$cyl,levels=c(4,6,8),
                     labels=c("4cyl","6cyl","8cyl"))
    $ 
    $ 
    $ #This graph shows cluster groups
    $ # MPG goes down by weight
    $ # Heavier calls have more cylinders
    $ # More cylinders may mean less MPG
    $ ggplot(mtcars, aes(wt, mpg, color = cyl)) +
    $   geom_point() +
    $   geom_smooth(method = "lm", formula = y~x) +
    $   labs(title = "Regression of MPG on Weight", x = "Weight", y = "Miles per Gallon")
    $ 
    $ 
    $ #Box plots are useful for showing outliers
    $ qplot(gear, mpg, data=mtcars, geom=c("boxplot", "jitter"),
    $       fill=gear, main="Mileage by Gear Number",
    $       xlab="", ylab="Miles per Gallon")
    $ 
    $ #Shows 1 outlier
    $ boxplot(mpg ~ vs, data=mtcars, main="Displacement")
    $ 
    $ 
    $ #Quick method for findign variable importance 
    $ modelFit <- train( mpg~.,data=mtcars, method="rf" ,importance = TRUE)
    $ varImp(modelFit)
    $ 
    $ #Find weights of bariable importance using regsubsets
    $ best.subset <- regsubsets(mpg~., mtcars, nvmax=5)
    $ 
    $ best.subset.summary <- summary(best.subset)
    $ 
    $ #This graph plots how adding more varaible adds to the adjusted R^2 value 
    $ #  which is how well the model does.   As you can see, after 3 vaiables it 
    $ #  doesn't really improve
    $ plot(best.subset.summary$adjr2, xlab="Number of Variables", ylab="Adjusted RSq", type="l")
    $ 
    $ #This shows qsec, weight and transmission are the most important variables
    $ plot(best.subset)
    $ 
    $ 
    $ #Relabel them for Linear model
    $ data(mtcars)
    $ mtcars$cyl <- factor(mtcars$cyl)
    $ mtcars$vs <- factor(mtcars$vs)
    $ mtcars$gear <- factor(mtcars$gear)
    $ mtcars$carb <- factor(mtcars$carb)
    $ #There are some issues using factors currenlty
	$ #mtcars$am <- factor(mtcars$am,levels=c(0,1))
    $ 
    $ #Create a linear regression model
    $ mtmodel <- lm(mpg ~ qsec + wt + am, data=mtcars)
    $ summary(mtmodel)
    $ 
    $ #Create a new set of data to predict
    $ newdata <- data.frame("qsec" = c(22.2,10.12), "wt" = c(2.6, 3.1), "am" = c(1,0) )
    $ #newdata$am <- factor(newdata$am,levels=c(0,1))
    $ 
    $ newdata$predicted_mpg = predict(mtmodel, newdata = newdata)
    $ 
    $ #print predicted values
    $ newdata
    $ 
    $ 
    $ saveRDS(object = mtmodel, file = 'C:\\Users\\Ryan\\Documents\\R_Projects\\ACUMOS\\rdsmodel', compress = 'gzip')




Testing
=======

We use a combination of ``tox``, ``pytest``, and ``flake8`` to test
``model_management``. Code which is not PEP8 compliant (aside from E501) will be
considered a failing test. You can use tools like ``autopep8`` to
“clean” your code as follows:

.. code:: bash

    $ pip install autopep8
    $ cd rds-model-runner
    $ autopep8 -r --in-place --ignore E501 predictor/ test/

Run tox directly:

.. code:: bash

    $ cd rds-model-runner
    $ tox

You can also specify certain tox environments to test:

.. code:: bash

    $ tox -e py34  # only test against Python 3.4
    $ tox -e flake8  # only lint code

And finally, you can run pytest directly in your environment *(recommended starting place)*:

.. code:: bash

    $ pytest
    $ pytest -s   # verbose output
