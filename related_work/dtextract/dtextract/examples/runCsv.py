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

import numpy as np
from sklearn.ensemble import RandomForestClassifier
from sklearn.tree import DecisionTreeRegressor

from ..data.data import *
from ..data.consts import *
from ..impl.funcs import *
from ..impl.dists import *
from ..impl.simp import *
from ..util.log import *
from ..util.util import *

# Parameters

# general training parameters
trainingProp = 0.6 # proportion of training data
cvProp = 0.3 # proportion of cv data

# Gaussian mixture model parameters
nComponents = 20

# random forest training parameters
nTrees = 1000

# decision tree extraction parameters
tgtScore = None
minGain = None
maxSize = 33

nPts = 500
nPtTries = 100
nTestPts = 500

# decision tree training parameters
nGreedyTries = 1
maxDtSize = maxSize

# printing parameters
names = ['rf train score: ', 'rf cv score: ', 'rf test score: ', 'extracted dt train score: ', 'extracted dt cv score: ', 'extracted dt test score: ', 'trained dt train score: ', 'trained dt cv score: ', 'trained dt test score: ']

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
#  return : float * float * float * float * float * float * float * float * float (the train, cv, test scores for the random forest, extracted decision tree, and trained decision tree)
def runCsvSingle(path, hasHeader, dataTypes, isClassify, nDataMatrixCols,distType):
    # Step 1: Learn random forest
    log('Parsing CSV...', INFO)
    (df, res, resMap, catFeats) = readCsv(path, hasHeader, dataTypes)
    log('Done!', INFO)

    log('Splitting into training and test...', INFO)
    (trainDfFull, testDf) = split(df, trainingProp + cvProp)
    (trainDf, cvDf) = split(trainDfFull, trainingProp / (trainingProp + cvProp))
    log('Done!', INFO)

    log('Constructing data matrices...', INFO)
    (XTrainFull, yTrainFull, catFeatIndsFull, numericFeatIndsFull) = \
        constructDataMatrix(trainDfFull, res, catFeats)
    (XTrain, yTrain, catFeatIndsTrain, numericFeatIndsTrain) = \
        constructDataMatrix(trainDf, res, catFeats)
    (XCv, yCv, catFeatIndsCv, numericFeatIndsCv) = \
        constructDataMatrix(cvDf, res, catFeats)
    (XTest, yTest, catFeatIndsTest, numericFeatIndsTest) = \
        constructDataMatrix(testDf, res, catFeats)
    assert(catFeatIndsFull == catFeatIndsTrain)
    assert(catFeatIndsFull == catFeatIndsCv)
    assert(catFeatIndsFull == catFeatIndsTest)
    assert(numericFeatIndsFull == numericFeatIndsTrain)
    assert(numericFeatIndsFull == numericFeatIndsCv)
    assert(numericFeatIndsFull == numericFeatIndsTest)
    log('Done!', INFO)

    log('Training random forest...', INFO)
    rf = RandomForestClassifier(n_estimators=nTrees)
    rf.fit(XTrain, yTrain)
    log('Done!', INFO)

    rfTrainScore = rf.score(XTrain, yTrain)
    rfCvScore = rf.score(XCv, yCv)
    rfTestScore = rf.score(XTest, yTest)
    
    log('Training score: ' + str(rfTrainScore), INFO)
    log('CV score: ' + str(rfCvScore), INFO)
    log('Test score: ' + str(rfTestScore), INFO)

    # Step 2: Set up decision tree extraction inputs
    paramsLearn = ParamsLearn(tgtScore, minGain, maxSize)
    paramsSimp = ParamsSimp(nPts, nTestPts, isClassify)

    # Step 3: Function
    rfFunc = getRfFunc(rf)

    # Step 4: Distribution
    if distType == 'CategoricalGaussianMixture':
        dist = CategoricalGaussianMixtureDist(XTrainFull, catFeatIndsFull, 
                numericFeatIndsFull, nComponents)
        #dist = GaussianMixtureDist(XTrainFull, nComponents)
    else:
        raise Exception('Invalid distType: ' + distType)
    
    # Step 5: Extract decision tree
    dtExtract = learnDTSimp(genAxisAligned, rfFunc, dist, paramsLearn, paramsSimp)

    log('Decision tree:', INFO)
    log(str(dtExtract), INFO)
    log('Node count: ' + str(dtExtract.nNodes()), INFO)

    dtExtractRelTrainScore = acc(dtExtract.eval, XTrain, rf.predict(XTrain))
    dtExtractRelCvScore = acc(dtExtract.eval, XCv, rf.predict(XCv))
    dtExtractRelTestScore = acc(dtExtract.eval, XTest, rf.predict(XTest))

    log('Relative training score: ' + str(dtExtractRelTrainScore), INFO)
    log('Relative CV score: ' + str(dtExtractRelCvScore), INFO)
    log('Relative test score: ' + str(dtExtractRelTestScore), INFO)
    
    dtExtractTrainScore = acc(dtExtract.eval, XTrain, yTrain)
    dtExtractCvScore = acc(dtExtract.eval, XCv, yCv)
    dtExtractTestScore = acc(dtExtract.eval, XTest, yTest)
    
    log('Training score: ' + str(dtExtractTrainScore), INFO)
    log('CV score: ' + str(dtExtractCvScore), INFO)
    log('Test score: ' + str(dtExtractTestScore), INFO)
    
    # Step 6: Train a (greedy) decision tree regressor, best out of nGreedyTries tries (on test score!)
    log('Training greedy decision tree, best of: ' + str(nGreedyTries), INFO)
    dtConstructor = DecisionTreeClassifier if isClassify else DecisionTreeRegressor
    maxDtLeaves = (maxDtSize + 1)/2
    cvScore = -1.0
    dtTrain = None
    for i in range(nGreedyTries):
        # train the tree (use randomness for i > 0 so there is variety
        dtTrainCur = dtConstructor(max_leaf_nodes = maxDtLeaves, splitter = ('best' if i == 0 else 'random'))
        dtTrainCur.fit(XTrain, yTrain)
        # score the tree
        cvScoreCur = dtTrainCur.score(XCv, yCv)
        # retain the highest scoring tree
        if cvScore < cvScoreCur:
            cvScore = cvScoreCur
            dtTrain = dtTrainCur
    log('Done!', INFO)
    log('Node count: ' + str(dtTrain.tree_.node_count), INFO)

    dtTrainTrainScore = dtTrain.score(XTrain, yTrain)
    dtTrainCvScore = dtTrain.score(XCv, yCv)
    dtTrainTestScore = dtTrain.score(XTest, yTest)

    log('Training score: ' + str(dtTrainTrainScore), INFO)
    log('CV score: ' + str(dtTrainCvScore), INFO)
    log('Test score: ' + str(dtTrainTestScore), INFO)

    return [rfTrainScore, rfCvScore, rfTestScore, dtExtractTrainScore, dtExtractCvScore, dtExtractTestScore, dtTrainTrainScore, dtTrainCvScore, dtTrainTestScore]

# Runs the CSV example repeatedly and reports the average values.
#
# parameters/returns:
#  path : str (path to csv containing dataset)
#  hasHeader : bool (whether the csv has a header)
#  dataTypes : [int] (labels for dataset column data types)
#  isClassify : bool (classification vs. regression)
#  nDataMatrixCols : int (the number of columns in the constructed data matrix)
#  distType: "SamplePlusGauss" | "CategoricalGaussianMixture", the type of distribution, default "CategoricalGaussianMixture"
#  nRepeats : int (default : 1) (number of repetitions to compute the average)
def runCsv(path, hasHeader, dataTypes, isClassify, nDataMatrixCols, distType = "CategoricalGaussianMixture", nRepeats=1):
    # initialize vals
    nVals = len(names)
    vals = [0.0 for i in range(nVals)]

    # obtain averages
    for i in range(nRepeats):
        curVals = runCsvSingle(path, hasHeader, dataTypes, isClassify, nDataMatrixCols, distType)
        for j in range(nVals):
            vals[j] += curVals[j]

    # normalize
    for i in range(nVals):
        vals[i] /= float(nRepeats)

    for i in range(nVals):
        print(names[i] + str(vals[i]))
