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

from scipy.stats import truncnorm
from scipy.stats import norm
import numpy as np

from sklearn import metrics


from .log import *

# Computes the accuracy of the given function on the
# given points
#
# type parameters:
#  X : input domain
#  Y : output domain
#
# parameters/returns:
#  func : X -> Y
#  xs : [X]
#  ys : [Y]
#  return : float


def acc(func, xs, ys):
    if len(xs) != len(ys):
        raise Exception('Invalid inputs!')
    tot = 0
    for i in range(len(xs)):
        if func(xs[i]) == ys[i]:
            tot += 1
    return float(tot) / float(len(xs))

# Computes the accuracy of the given approximation of the
# given function on the given points.
#
# type parameters:
#  X : input domain
#  Y : output domain
#
# parameters/returns:
#  func : X -> Y
#  approx : X -> Y
#  xs : [X]
#  return : float


def accSet(func, approx, xs):
    # Sum the number of points where the func and approx agree
    inds = [1 if func(x) == approx(x) else 0 for x in xs]
    return float(sum(inds)) / float(len(xs))

# Estimates the accuracy of the given approximation of the
# given function over the given distribution using the
# given number of points.
#
# type params:
#  X : input domain
#  Y : output domain
#
# parameters/returns:
#  func : X -> Y
#  approx : X -> Y
#  dist : () -> X
#  nPts : int
#  return : float


def accDist(func, approx, dist, nPts):
    # Step 1: Sample random points
    xs = [dist() for i in range(nPts)]
    # Step 2: Return the accuracy on the sampled points
    return accSet(func, approx, xs)

# Computes the accuracy of the given function on the
# given points
#
# type parameters:
#  X : input domain
#  Y : output domain
#
# parameters/returns:
#  func : X -> Y
#  xs : [X]
#  ys : [Y]
#  return : float


def _f1_old(yPreds, xs, ys):
    if len(xs) != len(ys):
        raise Exception('Invalid inputs!')
    tp = 0
    fp = 0
    fn = 0
    for i in range(len(xs)):
        if yPreds[i] == 1:
            if ys[i] == 1:
                tp += 1
            else:
                fp += 1
        else:
            if ys[i] == 1:
                fn += 1

    prec = float(tp) / float(tp + fp) if tp + fp != 0 else 0.0
    rec = float(tp) / float(tp + fn) if tp + fn != 0 else 0.0

    return 2.0 * prec * rec / (prec + rec) if prec + rec != 0.0 else 0.0


def _f1(yPreds, xs, ys):
    log(metrics.classification_report(ys, yPreds, digits=3), INFO)
    report = metrics.classification_report(ys, yPreds, digits=3, output_dict=True)
    return report['weighted avg']['f1-score']


def f1(func, xs, ys):
    return _f1([func(x) for x in xs], xs, ys)


def f1Vec(func, xs, ys):
    return _f1(func(xs), xs, ys)

# Computes the MSE of the given function on the
# given points
#
# type parameters:
#  X : input domain
#  Y : output domain
#
# parameters/returns:
#  func : X -> Y
#  xs : [X]
#  ys : [Y]
#  return : float


def _mse(yPreds, xs, ys):
    if len(xs) != len(ys):
        raise Exception('Invalid inputs!')
    diffs = [z[0] - z[1] for z in zip(yPreds, ys)]
    sqs = [z * z for z in diffs]
    return float(sum(sqs)) / float(len(xs))


def mse(func, xs, ys):
    return _mse([func(x) for x in xs], xs, ys)


def mseVec(func, xs, ys):
    return _mse(func(xs), xs, ys)

# Estimates the mean squared error of the given
# approximation of the given function using the
# given points.
#
# type params:
#  X : input domain
#  Y = float : output domain
#
# parameters/returns:
#  func : X -> Y
#  approx : X -> Y
#  xs : [X]
#  return : float


def mseSet(func, approx, xs):
    # Sum the number of points where the func and approx agree
    diffs = [func(x) - approx(x) for x in xs]
    sqs = [y * y for y in diffs]
    return np.sqrt(float(sum(sqs)) / float(nPts))

# Estimates the mean squared error of the given
# approximation of the given function over the given
# distribution using the given number of points.
#
# type params:
#  X : input domain
#  Y = float : output domain
#
# parameters/returns:
#  func : X -> Y
#  approx : X -> Y
#  dist : () -> X
#  nPts : int
#  return : float


def mseDist(func, approx, dist, nPts):
    # Step 1: Sample random points
    xs = (dist() for i in range(nPts))
    # Step 2: Return MSE on the sampled points
    return np.sqrt(mseSet(func, approx, xs))


# Calculates integral under a 1-dimensional Gaussian with specified mean,
# standard deviation, and between the two ranges specified
# parameters/returns:
#  mean : float, mean of distribution
#  std: float, standard deviation of distribution
#  lower : float | -np.inf, lower limit of integral
#  upper : float | np.inf, upper limit of integral
#  return : float, area between the two limits
def integrateTruncated(mean, std, lower, upper):
    rv = norm(loc=mean, scale=std)
    if rv.cdf(upper) - rv.cdf(lower) == 0:
        log(("equals zero", upper, lower, mean, std), DEBUG)
    return rv.cdf(upper) - rv.cdf(lower)


# Calculates total density within a constrained rectangle of a Gaussian with
# specified mean and (diagonal) covariance matrix
#
#
# params/returns:
#  mean: np.array([nCols]), (multivariate) mean of the distribution
#  cov: np.array([nCols]), (multivariate) diagonal elements of the covariance matrix of the distribution, assumed diagonal
#  limits: [[float | np.inf | -np.inf]], a list of lists, each of which specifies an upper and lower bound
#    of the constrained region for that dimension
#  return: float
def constrainedGaussianDensity(mean, cov, limits):
    nCols = np.size(mean)
    totalDensity = 1
    for d in range(nCols):
        limit = limits[d]
        std = np.sqrt(cov[d])
        totalDensity = totalDensity * integrateTruncated(mean[d], std, limit[0], limit[1])

    return totalDensity


# Takes constraints of type C and turns it into a list of lists, two
# constraints per dimension
# type params:
#  C = [(InternalNode, bool)] (i.e., constraints are lists of internal nodes, and
#                              a boolean indicating left, x[ind] <= thresh (True)
#                              or right, x[ind] > thresh (False))
#
# params/returns:
#  cons: C, constraints
#  nCols: int, dimension of data
#  returns: [[float | np.inf | -np.inf]], each (sub)list specifies the two
#    (upper and lower) bounds of the constraints of the constrained region for that dimension
def consolidateConstraints(cons, nCols):
    # make a nCols-dimensional list of lists, each of which specifies an
    # upper and lower bound of the constrained region for that dimension
    limits = [[-np.inf, np.inf] for i in range(nCols)]
    for con in cons:
        ind = con[0].ind
        thresh = con[0].thresh
        if con[1]:
            # upper limit
            curUpperLim = limits[ind][1]
            if thresh < curUpperLim:
                limits[ind][1] = thresh
        else:
            # lower limit
            curLowerLim = limits[ind][0]
            if thresh > curLowerLim:
                limits[ind][0] = thresh
    return limits


# samples from a multidimensional truncated diagonal-covariance gaussian
#
# params/returns:
#  mean: np.array([nCols]), mean of Gaussian
#  cov: np.array([nCols]), diaganal elements of (assume diagonal) covariance matrix
#    of Gaussian
#  limits: [[float | np.inf | -np.inf]], a list of lists, each (sub)list specifies the two (upper and lower)
#    bounds of the constraints
#  nPts: number of points to sample
#  returns: np.array([nPts, nCols]), samples from the multivariate Gaussian
def sampleTruncGaussian(mean, cov, limits, nPts):
    nCols = len(limits)
    samples = np.zeros((nCols, nPts))
    for i in range(nCols):
        limit = limits[i]
        mu = mean[i]
        std = np.sqrt(cov[i])
        a, b = (limit[0] - mu) / std, (limit[1] - mu) / std
        samples[i, :] = truncnorm.rvs(a, b, loc=mu, scale=std, size=nPts)
    return samples.transpose()

# Calculates total density within rectangular constraints of a Gaussian
# Mixture Model
#
# params/returns:
#  means: np.array(numComponents, nCols), means of the Gaussians
#  covariances: np.array(numComponents, nCols), covariances of the Gaussians
#    (with diagonal covariance matrices)
#  numComponents: int, number of components in the Gaussian mixture model
#  returns: float


def totalDensityGaussianMixture(means, covariances, weights, numComponents):
    totalDensity = 0.0
    for component in range(numComponents):
        mean = means[component]
        cov = covariances[component]
        weight = weights[component]
        totalDensity = totalDensity + \
            constrainedGaussianDensity(mean, cov, limits) * weight
    return totalDensity
