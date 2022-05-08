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
from sklearn.mixture import GaussianMixture

from ..util.log import *
from ..util.util import *

# Implementation of useful distributions.

# Fits a Gaussian mixture model with the given number of components.
#
# fields:
#  X : np.array([nRows, nCols]) (the example points)
#  num_components : int, number of components to fit


class GaussianMixtureDist:
    def __init__(self, X, numComponents):
        self.gmm = GaussianMixture(
            n_components=numComponents, covariance_type="diag", reg_covar=100
        )
        self.nCols = np.shape(X)[1]
        self.numComponents = numComponents
        # fit a Gaussian mixture model
        log(
            "Fitting Gaussian mixture with {} components and {} columns ...".format(
                str(numComponents), str(self.nCols)
            ),
            INFO,
        )
        self.gmm.fit(X)
        log("Done!", INFO)

    # Samples a random point from the fitted mixture model
    def sampleUnconstrained(self):
        return np.array((self.gmm.sample())[0][0, :])

    # Compute the probability of each component in the mixture
    def _computeProbabilities(self, limits):
        probabilities = np.zeros(self.numComponents)
        for component in range(self.numComponents):
            mean = self.gmm.means_[component]
            cov = self.gmm.covariances_[component]
            weight = self.gmm.weights_[component]
            probabilities[component] = (
                constrainedGaussianDensity(mean, cov, limits) * weight
            )
        return probabilities

    # Integrate the probability density given the constraints.
    def mass(self, limits):
        probabilities = self._computeProbabilities(limits)
        return np.sum(probabilities)

    # Samples a random point from the fitted mixture model
    # given the constraints
    #
    # returns: np.array([nPts, self.nCols])
    def sample(self, limits, nPts):
        # consolidate constraints
        # limits = consolidateConstraints(cons, self.nCols)

        # compute probabilities
        probabilities = self._computeProbabilities(limits)

        # compute mass
        s = np.sum(probabilities)

        log(("probabilities per component:", probabilities), DEBUG)
        log(("limits:", limits), DEBUG)

        # density is zero (up to rounding) within these constraints
        xs = np.zeros((nPts, self.nCols))
        if s == 0:
            return xs

        # normalize
        probabilities = probabilities / s

        # Count of how many points to sample
        chosenComponents = np.random.choice(
            self.numComponents, size=nPts, p=probabilities
        )

        # Sample the points
        curIndex = 0
        for component in range(self.numComponents):
            curCount = np.sum(chosenComponents == component)
            nextIndex = curIndex + curCount
            xs[curIndex:nextIndex, :] = sampleTruncGaussian(
                self.gmm.means_[component],
                self.gmm.covariances_[component],
                limits,
                curCount,
            )
            curIndex = nextIndex

        return xs


# Given indicator form of one categorical variable, fits and samples from it
# fields:
#  X : np.array([nRows, numCats]), each element is 0 or 1


class CategoricalDist:
    def __init__(self, X):
        self.numCats = np.shape(X)[1]
        probSum = np.sum(X, axis=0)
        self.probs = probSum / float(np.sum(probSum))

    def sample(self, limits, nPts):
        # Step 1: Construct probabilities given limits
        probs = np.copy(self.probs)
        for c in range(self.numCats):
            # Step 1a: Collect the indicators that work
            allowedInds = []
            for ind in [0, 1]:
                if limits[c][0] < ind and ind <= limits[c][1]:
                    allowedInds.append(ind)

            # Step 1b: No indicators
            if len(allowedInds) == 0:
                raise Exception("No points satisfy constraints for a category!")

            # Step 1c: Single indicator
            if len(allowedInds) == 1:
                # forced to be one (we assume this can only happen once)
                if allowedInds[0] == 1:
                    xs = np.zeros((nPts, self.numCats), dtype=int)
                    xs[:, c] = 1
                    return xs
                # forced to be zero
                else:
                    probs[c] = 0.0

        # Step 2: Normalize probabilities
        probs = probs / np.sum(probs)

        # Step 3: Sample points
        sampled_cats = np.random.choice(self.numCats, nPts, p=probs)

        # Step 4: Construct points
        xs = np.zeros((nPts, self.numCats), dtype=int)
        xs[np.arange(nPts), sampled_cats] = 1

        return xs

    def mass(self, limits):
        # Step 1: Construct probabilities given limits
        probSum = 1.0
        constrainedCat = None
        for c in range(self.numCats):
            # Step 1a: Collect the indicators that work
            allowedInds = []
            for ind in [0, 1]:
                if limits[c][0] < ind and ind <= limits[c][1]:
                    allowedInds.append(ind)

            # Step 1b: No indicators
            if len(allowedInds) == 0:
                raise Exception("No points satisfy constraints for a category!")

            # Step 1c: Single indicator
            if len(allowedInds) == 1:
                # forced to be one (we assume this can only happen once)
                if allowedInds[0] == 1:
                    return self.probs[c]
                # forced to be zero
                else:
                    probSum -= self.probs[c]

        return probSum


# Fields:
#  catFeatInds: list of (# of categorical features) lists, each of (# categories
#       per categorical feature) listing the column indices that correspond to that
#       feature in X)
#  numericFeatInds: list of column indices that correspond to numeric features in X


class CategoricalGaussianMixtureDist:
    def __init__(self, X, catFeatInds, numericFeatInds, numComponents):
        self.catFeatInds = catFeatInds
        self.numericFeatInds = numericFeatInds
        self.categoricalDist = []
        for featureInd in catFeatInds:
            self.categoricalDist.append(CategoricalDist(X[:, featureInd]))
        if len(numericFeatInds) == 0:
            self.GMDist = None
        else:
            self.GMDist = GaussianMixtureDist(X[:, numericFeatInds], numComponents)
        self.nCols = np.shape(X)[1]

    def sample(self, cons, nPts):
        xs = np.empty((nPts, self.nCols))
        limits = consolidateConstraints(cons, self.nCols)

        for feature in range(len(self.catFeatInds)):
            catDist = self.categoricalDist[feature]
            catFeatInd = self.catFeatInds[feature]
            cat_xs = catDist.sample([limits[cF] for cF in catFeatInd], nPts)
            xs[:, catFeatInd] = cat_xs
        if not self.GMDist is None:
            numeric_xs = self.GMDist.sample(
                [limits[nF] for nF in self.numericFeatInds], nPts
            )
            xs[:, self.numericFeatInds] = numeric_xs
        return xs

    def mass(self, cons):
        limits = consolidateConstraints(cons, self.nCols)
        mass = 1
        for feature in range(len(self.catFeatInds)):
            catFeatInd = self.catFeatInds[feature]
            catDist = self.categoricalDist[feature]
            mass *= catDist.mass([limits[cF] for cF in catFeatInd])
        if not self.GMDist is None:
            mass *= self.GMDist.mass([limits[nF] for nF in self.numericFeatInds])
        return mass


#
# TODO: Functions below are not up to date.
#

# Distribution given as a lambda.
#
# type parameters:
#  X : input domain
#
# fields:
#  dist : () -> (X | None)
class LambdaDist:
    def __init__(self, dist):
        self.dist = dist

    # Samples a random point.
    #
    # parameters/returns:
    #  return : () -> np.array([nCols])
    def sample(self):
        return self.dist()


# Chooses a random example point, and adds Gaussian noise
# to that point with the given covariance matrix.
#
# fields:
#  X : np.array([nRows, nCols]) (the example points)
#  sigmas : np.array([nCols]) (the desired standard deviations)


class XPlusGaussDist:
    def __init__(self, X, sigmas):
        self.X = X
        self.sigmas = sigmas

    # Samples a random point.
    #
    # parameters/returns:
    #  return : () -> np.array([nCols])
    def sample(self):
        (nRows, nCols) = self.X.shape
        # Step 1: Sample a random example point x
        row = random.randint(0, nRows - 1)
        # Step 2: Sample the noise \epsilon
        epsilon = [random.gauss(0, self.sigmas[i]) for i in range(nCols)]
        # Step 3: Return x + \epsilon
        return self.X[row, :] + np.array(epsilon)


# Rejection sampling. Fails after given number of tries.
#
# type params:
#  X : input domain
#  C = [(InternalNode, bool)] (i.e., constraints are lists of internal nodes, and
#                              a boolean indicating left, x[ind] <= thresh (True)
#                              or right, x[ind] > thresh (False))
#
# fields:
#  dist : {sample : () -> (X | None)}
#  nTries : int


class RejectionSampler:
    def __init__(self, dist, nTries):
        self.dist = dist
        self.nTries = nTries

    # Sample a point using rejection sampling.
    #
    # parameters/returns:
    #  cons : C
    #  return : X | None
    def sample(self, cons, nPts):
        xs = []
        for i in range(nPts):
            x = self._sampleHelper(cons)
            if not x is None:
                xs.append(x)
        return xs

    # Samples a single point.
    def _sampleHelper(self, cons):
        for i in range(self.nTries):
            x = self.dist.sample()
            if _satisfies(x, cons):
                return x
        return None

    # Estimate the mass using sampling.
    def mass(self, cons):
        count = 0
        for i in range(self.nTries):
            x = self.dist.sample()
            if _satisfies(x, cons):
                count += 1
        return float(count) / self.nTries


# Checks whether a point satisfies the list of constraints.


def _satisfies(x, cons):
    for con in cons:
        # Evaluating con[0].eval(x) yields True (left) vs. False (right).
        # The branch taken is left (con[1] == True) vs. right (con[1] == False).
        # Hence, con[0].eval(x) == con[1] if con is satisfied by x.
        if con[0].eval(x) != con[1]:
            return False
    return True
