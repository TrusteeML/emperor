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

from sklearn.tree import DecisionTreeClassifier
from sklearn.tree import DecisionTreeRegressor
import numpy as np

from ..util.log import *

# Parameters for baseline learner
#
# fields:
#  nPts : int (number of points to sample)
#  isClassify : bool (whether to use a classifier or a regressor)
#  maxSize : int (maximum size of the decision tree)
#  minGain : float (minimum gain before stopping)


class ParamsBase:
    def __init__(self, nPts, isClassify, maxSize, minGain):
        self.nPts = nPts
        self.isClassify = isClassify
        self.maxSize = maxSize
        self.minGain = minGain

# Learn a decision tree using standard decision tree learning algorithm.
# Samples the specified number of points from the distribution, and then
# uses these points to train a decision tree.
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
#  dist        : D
#  params      : P
#  return      : DecisionTreeClassifier | DecisionTreeRegressor


def learnDTBase(func, dist, params):
    # Step 1: Sample points from the constrained distribution.
    log('Sampling ' + str(params.nPts) + ' points', INFO)
    xs = dist.sample([], params.nPts)
    ys = func(xs)
    log('Done! Sampled ' + str(len(xs)) + ' points', INFO)

    # Step 2: Classifier vs. regressor
    dtConstructor = DecisionTreeClassifier if params.isClassify else DecisionTreeRegressor

    # Step 3: Construct internal node
    log('Training decision tree with number of samples ' + str(params.nPts) + '...', INFO)
    maxLeaves = (params.maxSize + 1) / 2
    minGain = 0.0 if params.minGain is None else params.minGain
    dt = dtConstructor(max_leaf_nodes=maxLeaves, min_impurity_split=minGain)
    dt.fit(xs, ys)
    log('Done!', INFO)

    return dt
