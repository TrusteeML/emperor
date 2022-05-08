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
import pandas as pd

from dtextract.util.log import *

CAT = 0  # categorical data type
NUM = 1  # numeric data type
ID = 2  # identifier (to be ignored)
NUM_RES = 3  # numeric response
CAT_RES = 4  # categorical response

# Splits the dataset into two randomly selected sets according to
# the given proportion.
#
# parameters/returns:
#  df : pandas.DataFrame
#  prop : float (the proportion of training points, typically ~70%)
#  return : (DataTable, DataTable) (the (training, test) datasets)


def split(df, prop):
    # Checks
    if prop < 0.0 or prop > 1.0:
        raise Exception("Invalid proportion: " + str(prop))

    # Step 1: Shuffle the row indices
    rows = [i for i in range(len(df))]
    random.shuffle(rows)

    # Step 2: Split into training and test rows
    splitPoint = int(prop * len(df))
    trainRows = rows[:splitPoint]
    testRows = rows[splitPoint:]

    # Step 2: Split data frame into train and test sets
    trainDf = df.iloc[trainRows, :]
    testDf = df.iloc[testRows, :]

    return (trainDf, testDf)


def constructDataMatrix(df, res, catFeats):
    # Step 1: Construct covariate and response columns
    covCols = []
    resCols = []
    catFeatIndices = [[] for cFeature in catFeats]
    numericFeatIndices = []
    for i in range(len(df.columns)):
        log("i:" + str(i) + " df.columns[i]:" + str(df.columns[i]), INFO)
        if df.columns[i] != res:
            categorical = False
            for j in range(len(catFeats)):
                cF = catFeats[j]
                if str(df.columns[i]).startswith(str(cF) + "_"):
                    categorical = True
                    catFeatIndices[j].append(len(covCols))
                    log(
                        "i:" + str(i) + " df.columns[i]:" + str(df.columns[i]) + " catFeat:" + str(cF),
                        INFO,
                    )
            if not categorical:
                numericFeatIndices.append(len(covCols))
            covCols.append(i)
        else:
            resCols.append(i)
    if len(resCols) != 1:
        raise Exception("Invalid columns!")

    # Step 2: Construct covariate and response data frames
    covDf = df.iloc[:, covCols]
    resDf = df.iloc[:, resCols]

    X = np.array(covDf.values)
    y = np.array(resDf.values[:, 0])

    return (X, y, catFeatIndices, numericFeatIndices)


# Parse the given CSV file and return a pandas DataFrame
# representation of the data.
#
# Note: The dataProcessors field is a list of lambdas that
#       are applied to the data in each column (in particular,
#       it should be the same length as the list dataTypes).
#       This field can be used to preprocess the data.
#
# parameters/returns:
#  path : str (path of the CSV file)
#  hasHeader : bool (whether the dataset has a header to ignore)
#  dataTypes : [int] (categorical, numeric, or identifier)
#  return : pandas.DataFrame


def readCsv(path, hasHeader, dataTypes, headers):
    # Step 1: Parse the CSV

    log("Reading file: " + path, INFO)

    # Step 1a: Skip the first row if it is the header
    skiprows = 1 if hasHeader else 0

    # Step 1b: Initialize data structures
    cur = 0
    names = []  # names
    dtype = {}  # data types
    impute = []  # impute these columns
    dummies = []  # convert these columns to indicators
    usecols = []  # list of columsn to use
    res = None
    isCatRes = None

    for i in range(len(dataTypes)):
        if not _isSkip(dataTypes[i]):
            # Step 1c: Append the name
            names.append(cur if not headers else headers[i])
            # Step 1d: Construct the data type
            dtype[cur if not headers else headers[i]] = _toDType(dataTypes[i])
            # Step 1e: Use this column
            usecols.append(i)
            # Step 1f: Add to impute if numeric
            if _isImpute(dataTypes[i]):
                impute.append(cur if not headers else headers[i])
            # Step 1g: Add to dummies if categorical
            if _isDummy(dataTypes[i]):
                dummies.append(cur if not headers else headers[i])
            # Step 1h: Handle response
            if _isResponse(dataTypes[i]):
                if res != None:
                    raise Exception("Multiple response variables!")
                res = cur if not headers else headers[i]
                isCatRes = _isCatResponse(dataTypes[i])
            # Step 1i: Increment the name
            cur += 1
        # else:
        #     names.append(-1)

    if res == None:
        raise Exception("No response variable!")

    # Step 1g: Parse the CSV
    df = pd.read_csv(
        path,
        header=None,
        skiprows=skiprows,
        usecols=usecols,
        names=names,
        dtype=dtype,
        na_values=["?"],
    )
    # df = pd.read_csv(path, usecols=usecols, dtype=dtype, names=names, na_values=['?'])

    log("Dataset shape: " + str(df.shape), INFO)

    # Step 2: Impute missing values for floating points
    for i in impute:
        df[i].fillna(df[i].mean(), inplace=True)

    # Step 3: Convert categorical to indicator
    df = pd.get_dummies(df, columns=dummies, dummy_na=False)

    # Step 4: If categorical response, convert to integer
    resMap = {}
    if isCatRes:
        # Step 4a: Construct response map
        for val in df[res]:
            if not val in resMap:
                resMap[val] = len(resMap)
        # Step 4b: Map response
        df[res] = df[res].apply(lambda val: resMap[val])

    log("Columns after: " + str(len(df.columns)), INFO)
    log(
        "Column names after:\n"
        + "".join((str(i) + ": " + str(col) + "\n" for (i, col) in zip(list(range(len(df.columns))), df.columns))),
        INFO,
    )

    df = df.replace([np.inf, -np.inf], np.nan).fillna(-1)

    return (df, res, resMap, dummies)


# Checks whether the datatype should be skipped (only ID).


def _isSkip(dataType):
    return dataType == ID


# Checks whether the data type should be imputed.


def _isImpute(dataType):
    return dataType == NUM


# Checks whether the data type should be converted from categorical to indicators.


def _isDummy(dataType):
    return dataType == CAT


# Checks whether the data type is a response type.


def _isResponse(dataType):
    return dataType == NUM_RES or dataType == CAT_RES


# Checks whether the data type is a categorical response.


def _isCatResponse(dataType):
    return dataType == CAT_RES


# Converts a data type to a pandas type.


def _toDType(dataType):
    if dataType == CAT or dataType == CAT_RES:
        return str
    elif dataType == NUM or dataType == NUM_RES:
        return np.float64
    elif dataType == ID:
        raise Exception("Should not consider ID types")
    else:
        raise Exception("Unknown data type: " + str(dataType))
