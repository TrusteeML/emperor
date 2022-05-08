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

import random

import numpy as np

from sklearn.tree import DecisionTreeClassifier, DecisionTreeRegressor

from ..core.learn import *
from ..util.log import *

# Parameters for simple learner.
#
# fields:
#  nPts : int (number of points to sample)
#  nTestPts : int (number of points to sample to estimate the score)
#  isClassify : bool (whether to use classifiers or regressors)


class ParamsSimp:
    def __init__(self, nPts, nTestPts, isClassify):
        self.nPts = nPts
        self.nTestPts = nTestPts
        self.isClassify = isClassify

# Learn a decision tree using standard decision tree learning algorithm.
# The constraints are lists of atomic constraints X -> bool, and include
# the atomic constraints of all ancestors of the current node or leaf.
# The distribution should return either a sample that satisfies the given
# constraints, or None (indicating failure).
#
# type parameters:
#  X = np.array([nCols])                           : input domain
#  Y = np.float                                    : output domain
#  XS = np.array([nPts, nCols])                    : list of inputs
#  YS = np.array([nPts])                           : list of outputs
#  C                                               : constraints (initialized to [])
#  D = {sample : C * int -> XS, mass : C -> float} : sampling distribution)
#  P                                               : parameters
#
# parameters/returns
#  func        : XS -> YS
#  gen         : (XS -> YS) * D * C * P -> (({eval : X -> bool} * C * C) | None) * float * {eval : X -> Y} * float
#                (given a function, sampling distribution, constraints, and parameters,
#                 generates a branch function, a leaf function, and estimates of the score for each)
#  dist        : D
#  paramsLearn : ParamsLearn
#  params      : P
#  return      : DT


def learnDTSimp(gen, func, dist, paramsLearn, params, featureNames=[]):
    return learnDT(lambda func, dist, cons: gen(func, dist, cons, params, featureNames=featureNames), func, dist, [], paramsLearn)

# Leaf nodes, encoded as a constant value to return.
#
# type parameters:
#  X = np.array([nCols]) : input domain
#  Y = np.float          : output domain
#
# fields:
#  val : Y


class LeafNode:
    def __init__(self, val):
        self.val = val

    # Evaluate the leaf node on the given input x.
    #
    # parameters/returns:
    #  x : X
    #  return : Y
    def eval(self, x):
        return self.val

    # Convert to string (just represents its constant value).
    def __str__(self):
        return str(self.val)

    def __lt__(self, other):
        return self.val < other.val

# Axis aligned branches, represented by an index (indicating the feature)
# and a threshold. The branch function is
#
#  B : X -> {0, 1}
#  B : x |-> I[x[ind] <= thresh]
#
# type parameters:
#  X = np.array([nCols]) : input domain
#
# fields:
#  ind : int
#  thresh : float


class InternalNode:
    def __init__(self, ind, thresh, label=""):
        self.ind = ind
        self.thresh = thresh
        self.label = label

    # Evaluate the branch for the given input x.
    #
    # parameters/returns:
    #  x : X
    #  return : bool
    def eval(self, x):
        return bool(x[self.ind] <= self.thresh)

    # Convert to string.
    def __str__(self):
        return '{} <= {}'.format(str(self.label), str(self.thresh)) if self.label else 'x[{}] <= {}'.format(str(self.ind), str(self.thresh))

    def __eq__(self, other):
        return self.ind == other.ind and self.thresh == other.thresh

    def __lt__(self, other):
        if not self.thresh or not other.thresh:
            return False
        return self.thresh < other.thresh


# Generates random axis-aligned features.
#
# type parameters:
#  X = np.array([nCols])                           : input domain
#  Y = np.float                                    : output domain
#  XS = np.array([nPts, nCols])                    : list of inputs
#  YS = np.array([nPts])                           : list of outputs
#  C = [(InternalNode, bool)]                      : (i.e., constraints are lists of internal nodes, and
#                                                     a boolean indicating left, x[ind] <= thresh (True)
#                                                     or right, x[ind] > thresh (False))
#  D = {sample : C * int -> XS, mass : C -> float} : sampling distribution)
#
# parameters/returns:
#  func : XS -> YS
#  dist : D
#  cons : C
#  params : ParamsSimp
#  return : (({eval : X -> bool} * C * C) | None) * float * {eval : X -> Y} * float * M * M


def genAxisAligned(func, dist, cons, params, featureNames=[]):
    # Step 1: Sample points from the constrained distribution.
    log('Sampling ' + str(params.nPts) + ' points', INFO)
    xs = dist.sample(cons, params.nPts)
    ys = func(xs)
    log('Done! Sampled ' + str(len(xs)) + ' points', INFO)

    # Step 3: If no points sampled, return a dummy leaf
    if len(xs) == 0:
        log('No points!', INFO)
        return ((InternalNode(None, None), None, None), 0.0, LeafNode(0.0), 0.0)  # (None, 0.0, LeafNode(0.0), 0.0)

    # Step 4: Classifier vs. regressor
    dtConstructor = DecisionTreeClassifier if params.isClassify else DecisionTreeRegressor

    # Step 5: Construct internal node data structure

    # Step 5a: Construct internal node
    log('Generating internal node with number of samples ' + str(params.nPts) + '...', INFO)
    dtInternal = dtConstructor(max_depth=1)
    dtInternal.fit(xs, ys)
    log('Done!', INFO)

    # Step 5b: Check internal node, construct data structure if valid
    if dtInternal.tree_.node_count != 3:
        log('Invalid internal node, node count: ' + str(dtInternal.tree_.node_count), INFO)
        dtInternalData = (InternalNode(None, None), None, None)
    else:
        featureName = "" if not featureNames else featureNames[dtInternal.tree_.feature[0]]
        dtInternalNode = InternalNode(dtInternal.tree_.feature[0], dtInternal.tree_.threshold[0], label=featureName)
        lcons = cons + [(dtInternalNode, True)]
        rcons = cons + [(dtInternalNode, False)]
        dtInternalData = (dtInternalNode, lcons, rcons)

    # Step 6: Construct leaf node data

    # Step 6a: Construct leaf node
    log('Generating leaf with number of samples ' + str(params.nPts) + '...', INFO)
    dtLeaf = dtConstructor(max_depth=1, min_samples_split=params.nPts + 1)
    dtLeaf.fit(xs, ys)
    log('Done!', INFO)

    # Step 6b: Check leaf node
    if dtLeaf.tree_.node_count != 1:
        raise Exception('Invalid leaf node, node count: ' + str(dtLeaf.tree_.node_count))

    # Step 6c: Construct data
    yPreds = set()  # We just use the first value here, but we use the entire set later to compute the gain
    for x in xs:
        yPreds.add(dtLeaf.predict(x.reshape(1, -1))[0])
    val = list(yPreds)[0]
    dtLeafData = LeafNode(val)

    # Step 7: Compute gain

    # Step 7a: Compute probability mass
    mass = dist.mass(cons)
    log('Current mass: ' + str(mass), INFO)

    # Step 7b: Sample test points
    log('Sampling ' + str(params.nPts) + ' test points', INFO)
    xsTest = dist.sample(cons, params.nPts)
    ysTest = func(xsTest)
    log('Done! Sampled ' + str(len(xsTest)) + ' test points', INFO)

    # Step 7c: Compute score of internal node and leaf node
    dtInternalScore = mass * dtInternal.score(xsTest, ysTest)
    dtLeafScore = mass * dtLeaf.score(xsTest, ysTest)
    log('Computed internal score: ' + str(dtInternalScore), INFO)
    log('Computed leaf score: ' + str(dtLeafScore), INFO)

    return (dtInternalData, dtInternalScore, dtLeafData, dtLeafScore)
