library(stats)
library(randomForest)
library(e1071)
library(tm)
library(RTextTools)

args <- commandArgs(trailingOnly=TRUE)
modelFile <- gzfile(args[1])
testData <- read.csv(args[2], check.names=FALSE)
model <- readRDS(modelFile)

classAttr <- attr(model, "class")
# TODO (pk9069): take length into consideration

if (classAttr == "custompredict") {
  predictionresults <- model$predict(testData)
} else if (classAttr == "gbm") {
  library(gbm)

  # TODO (pk9069): look into adding an additional parameter?
  digits <- nchar(trunc(model$n.trees))
  by = 100
  if (digits == 4) {
    by = 10
  } else if (digits == 3) {
    by = 5
  } else if (digits <= 2) {
    by = 1
  }

  # TODO (pk9069): figure out sequence
  n.trees = seq(from=1, to=model$n.trees, by=by)

  predictionresults <- predict(model, newdata=testData, n.trees=n.trees)
} else if (classAttr == "nn") {
  library(neuralnet)

  predictionresults <- compute(model, testData)
} else if (length(classAttr) >= 2 && classAttr[1] == "train" && classAttr[2] == "train.formula") {
  # K Nearest Neighbor

  library(caret)
  library(pROC)

  predictionresults <- predict(model, testData, type="prob")
} else if (classAttr == "adaboost") {
  library(JOUSBoost)

  predictionresults <- predict(model, testData)
} else if (classAttr == "kmeans") {
  # KMeans Clustering

  library(clue)
  predictionresults <- cl_predict(model, newdata=testData)
  predictionresults <- c(predictionresults)
} else if (classAttr == "ets" || (length(classAttr) >= 2 && classAttr[2] == "Arima")) {
  library(forecast)
  testData <- as.numeric(testData)
  predictionresults <- forecast(model, testData)
} else if (length(classAttr) >= 2 && classAttr[1] == "glm" && classAttr[2] == "lm") {
  predictionresults <- predict(model, newdata=testData, type="terms")
} else if (identical(model$call$x,NULL) == FALSE) {
  testcontainer <- create_container(testData, labels=as.factor(1:nrow(testData)), testSize=1:nrow(testData), virgin=FALSE)
  predictionresults <- classify_model(testcontainer, model)
} else if ('compprob' %in% names(model) && model$compprob) {
  predictionresults <- predict(model, newdata=testData, probability=TRUE)
  predictionresults <- attr(predictionresults, "probabilities")
} else {
  predictionresults <- predict(model, newdata=testData)
}

write.csv(predictionresults, args[3], row.names=FALSE)
