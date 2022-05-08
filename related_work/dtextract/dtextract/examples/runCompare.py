# Copyright 2015-2016 Stanford University
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http:#www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

import os
import numpy as np

from sklearn.neural_network import MLPClassifier
from sklearn.neural_network import MLPRegressor
from sklearn.ensemble import RandomForestClassifier
from sklearn.ensemble import RandomForestRegressor
from sklearn.tree import DecisionTreeClassifier
from sklearn.tree import DecisionTreeRegressor

from ..data.data import *
from ..data.consts import *
from ..impl.funcs import *
from ..impl.dists import *
from ..impl.simp import *
from ..impl.base import *
from ..util.log import *
from ..util.util import *
from ..util import persist

# Parameters

# general training parameters
trainingProp = 0.7  # proportion of training data

# Gaussian mixture model parameters
nComponents = 100

# model training parameters
useRandomForest = True

# random forest training parameters
nTrees = 1000

# neural net training parameters
hiddenSize = 500

# decision tree extraction parameters
tgtScore = None
minGain = None
maxSize = 200

nPts = 2000
nPtTries = 100
nTestPts = 2000

# decision tree training parameters
maxDtSize = maxSize

# printing parameters
names = [
    "rfTrainScore",
    "rfTestScore",
    "dtExtractRelTrainScore",
    "dtExtractRelTestScore",
    "dtExtractTrainScore",
    "dtExtractTestScore",
    "dtTrainRelTrainScore",
    "dtTrainRelTestScore",
    "dtTrainTrainScore",
    "dtTrainTestScore",
]

# This function
# (1) Loads the dataset
# (2) Trains a random forest
# (3) Extracts a decision tree from the trained random forest
#
# parameters/returns:
#  path : str (path to csv containing dataset)
#  hasHeader : bool (whether the csv has a header)
#  dataTypes : [int] (labels for dataset column data types)
#  isClassify : bool (classification vs. regression)
#  nDataMatrixCols : int (the number of columns in the constructed data matrix)
#  distType: 'CategoricalGaussianMixture' , the type of distribution
#  return : float * float * float (the relative accuracy according to the distribution for the extracted dt, trained dt, and lasso)


def runCompareSingle(
    path,
    hasHeader,
    dataTypes,
    isClassify,
    nDataMatrixCols,
    distType,
    headers,
    model=None,
    trainDf=None,
    testDf=None,
    res=0,
    catFeats=[],
    dtpath="",
):
    # Step 1: Learn random forest
    featureNames = []
    if trainDf is None and testDf is None:
        log("Parsing CSV...", INFO)
        (df, res, resMap, catFeats) = readCsv(path, hasHeader, dataTypes, headers)
        featureNames = list(df.columns)
        log("Done!", INFO)

        log("Splitting into training and test...", INFO)

        (trainDf, testDf) = split(df, trainingProp)
        log("Done!", INFO)

    log("Constructing data matrices...", INFO)
    (XTrain, yTrain, catFeatIndsTrain, numericFeatIndsTrain) = constructDataMatrix(trainDf, res, catFeats)
    (XTest, yTest, catFeatIndsTest, numericFeatIndsTest) = constructDataMatrix(testDf, res, catFeats)
    log("Done!", INFO)

    if model:
        rf = model
    else:
        if useRandomForest:
            log("Training random forest...", INFO)
            rfConstructor = RandomForestClassifier if isClassify else RandomForestRegressor
            rf = rfConstructor(n_estimators=nTrees)
            rf.fit(XTrain, yTrain)
            log("Done!", INFO)
        else:
            log("Training neural net...", INFO)
            rfConstructor = MLPClassifier if isClassify else MLPRegressor
            rf = rfConstructor(solver="lbfgs", hidden_layer_sizes=(hiddenSize,))
            rf.fit(XTrain, yTrain)
            log("Done!", INFO)

    rfScoreFunc = f1Vec if isClassify else mseVec

    rfTrainScore = rfScoreFunc(rf.predict, XTrain, yTrain)
    rfTestScore = rfScoreFunc(rf.predict, XTest, yTest)

    log("Training score: " + str(rfTrainScore), INFO)
    log("Test score: " + str(rfTestScore), INFO)

    # Step 2: Set up decision tree extraction inputs
    paramsLearn = ParamsLearn(tgtScore, minGain, maxSize)
    paramsSimp = ParamsSimp(nPts, nTestPts, isClassify)

    # Step 3: Function
    rfFunc = getRfFunc(rf)

    # Step 4: Distribution
    if distType == "CategoricalGaussianMixture":
        dist = CategoricalGaussianMixtureDist(XTrain, catFeatIndsTrain, numericFeatIndsTrain, nComponents)
    else:
        raise Exception("Invalid distType: " + distType)

    # Step 5: Extract decision tree
    dtExtract = learnDTSimp(genAxisAligned, rfFunc, dist, paramsLearn, paramsSimp, featureNames=featureNames)

    log("Decision tree:", INFO)
    log(str(dtExtract), INFO)
    log("Node count: " + str(dtExtract.nNodes()), INFO)
    dtExtract.plot(f"{dtpath}/dtExtract")

    scoreFunc = f1 if isClassify else mse

    dtExtractRelTrainScore = scoreFunc(dtExtract.eval, XTrain, rf.predict(XTrain))
    dtExtractRelTestScore = scoreFunc(dtExtract.eval, XTest, rf.predict(XTest))

    log("Relative training score: " + str(dtExtractRelTrainScore), INFO)
    log("Relative test score: " + str(dtExtractRelTestScore), INFO)

    dtExtractTrainScore = scoreFunc(dtExtract.eval, XTrain, yTrain)
    dtExtractTestScore = scoreFunc(dtExtract.eval, XTest, yTest)

    log("Training score: " + str(dtExtractTrainScore), INFO)
    log("Test score: " + str(dtExtractTestScore), INFO)

    # Step 6: Train a (greedy) decision tree
    log("Training greedy decision tree", INFO)
    maxLeaves = int((maxDtSize + 1) / 2)
    dtConstructor = DecisionTreeClassifier if isClassify else DecisionTreeRegressor
    dtTrain = dtConstructor(max_leaf_nodes=maxLeaves)
    dtTrain.fit(XTrain, rfFunc(XTrain))
    log("Done!", INFO)
    log("Node count: " + str(dtTrain.tree_.node_count), INFO)

    dtTrainRelTrainScore = scoreFunc(lambda x: dtTrain.predict(x.reshape(1, -1)), XTrain, rf.predict(XTrain))
    dtTrainRelTestScore = scoreFunc(lambda x: dtTrain.predict(x.reshape(1, -1)), XTest, rf.predict(XTest))

    log("Relative training score: " + str(dtTrainRelTrainScore), INFO)
    log("Relative test score: " + str(dtTrainRelTestScore), INFO)

    dtTrainTrainScore = scoreFunc(lambda x: dtTrain.predict(x.reshape(1, -1)), XTrain, yTrain)
    dtTrainTestScore = scoreFunc(lambda x: dtTrain.predict(x.reshape(1, -1)), XTest, yTest)

    log("Training score: " + str(dtTrainTrainScore), INFO)
    log("Test score: " + str(dtTrainTestScore), INFO)

    return [
        rfTrainScore,
        rfTestScore,
        dtExtractRelTrainScore,
        dtExtractRelTestScore,
        dtExtractTrainScore,
        dtExtractTestScore,
        dtTrainRelTrainScore,
        dtTrainRelTestScore,
        dtTrainTrainScore,
        dtTrainTestScore,
    ]


# Runs the CSV example repeatedly and reports the average values.
#
# parameters/returns:
#  path : str (path to csv containing dataset)
#  hasHeader : bool (whether the csv has a header)
#  dataTypes : [int] (labels for dataset column data types)
#  isClassify : bool (classification vs. regression)
#  nDataMatrixCols : int (the number of columns in the constructed data matrix)
#  output : str (name of output file)
#  distType: "SamplePlusGauss" | "CategoricalGaussianMixture", the type of distribution, default "GaussianMixture"
#  nRepeats : int (default : 1) (number of repetitions to compute the average)


def runCompare(
    path,
    hasHeader,
    dataTypes,
    isClassify,
    nDataMatrixCols,
    output,
    model=None,
    trainDf=None,
    testDf=None,
    res=0,
    catFeats=[],
    title="",
    distType="CategoricalGaussianMixture",
    nRepeats=1,
    headers=None,
):
    setCurOutput(output)
    dtpath = "./"
    with open(output) as f:
        dtpath = os.path.dirname(f.name)

    # initialize vals
    nVals = len(names)
    vals = [0.0 for i in range(nVals)]

    # obtain averages
    for i in range(nRepeats):
        curVals = runCompareSingle(
            path,
            hasHeader,
            dataTypes,
            isClassify,
            nDataMatrixCols,
            distType,
            headers,
            model=model,
            trainDf=trainDf,
            testDf=testDf,
            res=res,
            catFeats=catFeats,
            dtpath=dtpath,
        )
        for j in range(nVals):
            vals[j] += curVals[j]

    # normalize
    for i in range(nVals):
        vals[i] /= float(nRepeats)

    for i in range(nVals):
        log(names[i] + ": " + str(vals[i]), INFO)
