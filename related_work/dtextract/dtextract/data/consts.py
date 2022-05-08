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

from .data import *

# Constants

# Global constants

TMP_PATH = "res/tmp"
LOG_PATH = "res/log"

# Diabetes constants

DIABETES_PATH = TMP_PATH + "/dataset_diabetes/diabetic_data.csv"
DIABETES_HAS_HEADER = True
DIABETES_HEADERS = [
    "encounter_id",
    "patient_nbr",
    "race",
    "gender",
    "age",
    "weight",
    "admission_type_id",
    "discharge_disposition_id",
    "admission_source_id",
    "time_in_hospital",
    "payer_code",
    "medical_specialty",
    "num_lab_procedures",
    "num_procedures",
    "num_medications",
    "number_outpatient",
    "number_emergency",
    "number_inpatient",
    "diag_1",
    "diag_2",
    "diag_3",
    "number_diagnoses",
    "max_glu_serum",
    "A1Cresult",
    "metformin",
    "repaglinide",
    "nateglinide",
    "chlorpropamide",
    "glimepiride",
    "acetohexamide",
    "glipizide",
    "glyburide",
    "tolbutamide",
    "pioglitazone",
    "rosiglitazone",
    "acarbose",
    "miglitol",
    "troglitazone",
    "tolazamide",
    "examide",
    "citoglipton",
    "insulin",
    "glyburide-metformin",
    "glipizide-metformin",
    "glimepiride-pioglitazone",
    "metformin-rosiglitazone",
    "metformin-pioglitazone",
    "change",
    "diabetesMed",
    "readmitted",
]

DIABETES_DATA_TYPES = (
    [
        ID,
        ID,
        CAT,
        CAT,
        CAT,
        CAT,
        CAT,
        CAT,
        CAT,
        NUM,
        CAT,
        CAT,
        NUM,
        NUM,
        NUM,
        NUM,
        NUM,
        NUM,
        CAT,
        CAT,
        CAT,
        NUM,
    ]
    + [CAT for i in range(27)]
    + [CAT_RES]
)

DIABETES_IS_CLASSIFY = True
DIABETES_N_DATA_MATRIX_COLS = 2518

DIABETES_OUTPUT = LOG_PATH + "/diabetes.log"


# Iris constants

IRIS_PATH = TMP_PATH + "/iris.data"
IRIS_HAS_HEADER = False
IRIS_DATA_TYPES = [NUM, NUM, NUM, NUM, CAT_RES]

IRIS_IS_CLASSIFY = True
IRIS_N_DATA_MATRIX_COLS = 4

IRIS_OUTPUT = LOG_PATH + "/iris.log"

# Wine constants

WINE_PATH = TMP_PATH + "/wine.data"
WINE_HAS_HEADER = False
WINE_DATA_TYPES = [CAT_RES] + [NUM for i in range(13)]

WINE_IS_CLASSIFY = True
WINE_N_DATA_MATRIX_COLS = 13

WINE_OUTPUT = LOG_PATH + "/wine.log"

# Student constants

# Returns the type of val.


def getType(val):
    if val.__class__ == type(""):
        return CAT
    if val.__class__ == type(0.0) or val.__class__ == type(0):
        return NUM
    raise Exception("Invalid type: " + str(val))


STUDENT_PATH = TMP_PATH + "/student.csv"
STUDENT_HAS_HEADER = True
STUDENT_HEADERS = [
    "id",
    "school",
    "sex",
    "age",
    "address",
    "famsize",
    "Pstatus",
    "Medu",
    "Fedu",
    "Mjob",
    "Fjob",
    "reason",
    "nursery",
    "internet",
    "guardian.x",
    "traveltime.x",
    "studytime.x",
    "failures.x",
    "schoolsup.x",
    "famsup.x",
    "paid.x",
    "activities.x",
    "higher.x",
    "romantic.x",
    "famrel.x",
    "freetime.x",
    "goout.x",
    "Dalc.x",
    "Walc.x",
    "health.x",
    "absences.x",
    "G1.x",
    "G2.x",
    "G3.x",
    "guardian.y",
    "traveltime.y",
    "studytime.y",
    "failures.y",
    "schoolsup.y",
    "famsup.y",
    "paid.y",
    "activities.y",
    "higher.y",
    "romantic.y",
    "famrel.y",
    "freetime.y",
    "goout.y",
    "Dalc.y",
    "Walc.y",
    "health.y",
    "absences.y",
    "y",
]

STUDENT_EXAMPLE = [
    "GP",
    "F",
    15,
    "R",
    "GT3",
    "T",
    1,
    1,
    "at_home",
    "other",
    "home",
    "yes",
    "yes",
    "mother",
    2,
    4,
    1,
    "yes",
    "yes",
    "yes",
    "yes",
    "yes",
    "no",
    3,
    1,
    2,
    1,
    1,
    1,
    2,
    7,
    10,
    10,
    "mother",
    2,
    4,
    0,
    "yes",
    "yes",
    "yes",
    "yes",
    "yes",
    "no",
    3,
    1,
    2,
    1,
    1,
    1,
    4,
]
STUDENT_DATA_TYPES = [ID] + [getType(val) for val in STUDENT_EXAMPLE] + [NUM_RES]

STUDENT_IS_CLASSIFY = False
STUDENT_N_DATA_MATRIX_COLS = 492

STUDENT_OUTPUT = LOG_PATH + "/student.log"
STUDENT_FEATURE_OUTPUT = LOG_PATH + "/student_feature.log"

# Prostate cancer constants

PROSTATE_PATH = TMP_PATH + "/prostate.csv"
PROSTATE_HAS_HEADER = True
PROSTATE_EXAMPLE = [
    -0.776528789,
    3.539509,
    47,
    -1.38629436,
    0,
    -1.38629436,
    "6",
    0,
    1.047319,
]
PROSTATE_DATA_TYPES = [ID] + [getType(val) for val in PROSTATE_EXAMPLE] + [CAT_RES]
PROSTATE_IS_CLASSIFY = True
PROSTATE_N_DATA_MATRIX_COLS = 113

PROSTATE_OUTPUT = LOG_PATH + "/prostate.log"

# Car loan dataset

CAR_LOAN_PATH = TMP_PATH + "/car_loan.csv"
CAR_LOAN_HAS_HEADER = True
CAR_LOAN_EXAMPLE = [
    1,
    755,
    "PA",
    "F",
    "2003-09-29",
    "2003-09-29",
    "2003-10-06",
    72,
    4.95,
    5.35,
    30015,
    "NA",
    "N",
    4.99,
    4.95,
    1.12,
    414,
    59,
    14,
    4,
    3.419642857,
    -0.035714286,
    482.6937254,
    0.01608175,
    2,
    1,
]
CAR_LOAN_DATA_TYPES = [ID] + [getType(val) for val in CAR_LOAN_EXAMPLE] + [CAT_RES]
CAR_LOAN_IS_CLASSIFY = True
CAR_LOAN_N_DATA_MATRIX_COLS = 2377

CAR_LOAN_OUTPUT = LOG_PATH + "/car_loan.log"

# Breast cancer dataset

BREAST_CANCER_DIAG_PATH = TMP_PATH + "/breast_cancer_diag.data"
BREAST_CANCER_DIAG_HAS_HEADER = False
BREAST_CANCER_DIAG_EXAMPLE = [
    17.99,
    10.38,
    122.8,
    1001,
    0.1184,
    0.2776,
    0.3001,
    0.1471,
    0.2419,
    0.07871,
    1.095,
    0.9053,
    8.589,
    153.4,
    0.006399,
    0.04904,
    0.05373,
    0.01587,
    0.03003,
    0.006193,
    25.38,
    17.33,
    184.6,
    2019,
    0.1622,
    0.6656,
    0.7119,
    0.2654,
    0.4601,
    0.1189,
]
BREAST_CANCER_DIAG_DATA_TYPES = [ID, CAT_RES] + [getType(val) for val in BREAST_CANCER_DIAG_EXAMPLE]
BREAST_CANCER_DIAG_IS_CLASSIFY = True
BREAST_CANCER_DIAG_N_DATA_MATRIX_COLS = 31

BREAST_CANCER_DIAG_OUTPUT = LOG_PATH + "/breast_cancer_diag.log"

BREAST_CANCER_PROG_PATH = TMP_PATH + "/breast_cancer_prog.data"
BREAST_CANCER_PROG_HAS_HEADER = False
BREAST_CANCER_PROG_EXAMPLE = [
    18.02,
    27.6,
    117.5,
    1013,
    0.09489,
    0.1036,
    0.1086,
    0.07055,
    0.1865,
    0.06333,
    0.6249,
    1.89,
    3.972,
    71.55,
    0.004433,
    0.01421,
    0.03233,
    0.009854,
    0.01694,
    0.003495,
    21.63,
    37.08,
    139.7,
    1436,
    0.1195,
    0.1926,
    0.314,
    0.117,
    0.2677,
    0.08113,
    5,
    5,
]

BREAST_CANCER_PROG_CL_DATA_TYPES = [ID, CAT_RES, ID] + [getType(val) for val in BREAST_CANCER_PROG_EXAMPLE]
BREAST_CANCER_PROG_CL_IS_CLASSIFY = True
BREAST_CANCER_PROG_CL_N_DATA_MATRIX_COLS = 33

BREAST_CANCER_PROG_CL_OUTPUT = LOG_PATH + "/breast_cancer_prog_cl.log"

BREAST_CANCER_PROG_RG_DATA_TYPES = [ID, ID, NUM_RES] + [getType(val) for val in BREAST_CANCER_PROG_EXAMPLE]
BREAST_CANCER_PROG_RG_IS_CLASSIFY = False
BREAST_CANCER_PROG_RG_N_DATA_MATRIX_COLS = 33

BREAST_CANCER_PROG_RG_OUTPUT = LOG_PATH + "/breast_cancer_prog_rg.log"

BREAST_CANCER_PROG_MIX_DATA_TYPES = [ID, CAT_RES, NUM] + [getType(val) for val in BREAST_CANCER_PROG_EXAMPLE]
BREAST_CANCER_PROG_MIX_IS_CLASSIFY = True
BREAST_CANCER_PROG_MIX_N_DATA_MATRIX_COLS = 34

BREAST_CANCER_PROG_MIX_OUTPUT = LOG_PATH + "/breast_cancer_prog_mix.log"

# Car value dataset

CAR_PATH = TMP_PATH + "/car.data"
CAR_HAS_HEADER = False
CAR_DATA_TYPES = [CAT for i in range(6)] + [CAT_RES]
CAR_IS_CLASSIFY = True
CAR_N_DATA_MATRIX_COLS = 28

CAR_OUTPUT = LOG_PATH + "/car.log"

# Dermatology dataset

DERMATOLOGY_PATH = TMP_PATH + "/dermatology.data"
DERMATOLOGY_HAS_HEADER = False
DERMATOLOGY_DATA_TYPES = [NUM for i in range(33)] + [NUM, CAT_RES]
DERMATOLOGY_IS_CLASSIFY = True
DERMATOLOGY_N_DATA_MATRIX_COLS = 164

DERMATOLOGY_OUTPUT = LOG_PATH + "/dermatology.log"

# Fertility dataset

FERTILITY_PATH = TMP_PATH + "/fertility.txt"
FERTILITY_HAS_HEADER = False
FERTILITY_DATA_TYPES = [NUM, NUM, CAT, CAT, CAT, CAT, NUM, CAT, NUM, CAT_RES]
FERTILITY_IS_CLASSIFY = True
FERTILITY_N_DATA_MATRIX_COLS = 22

FERTILITY_OUTPUT = LOG_PATH + "/fertility.log"

# Post operative dataset

POST_OPERATIVE_PATH = TMP_PATH + "/post_operative.data"
POST_OPERATIVE_HAS_HEADER = False
POST_OPERATIVE_DATA_TYPES = [CAT, CAT, CAT, CAT, CAT, CAT, CAT, CAT, CAT_RES]
POST_OPERATIVE_IS_CLASSIFY = True
POST_OPERATIVE_N_DATA_MATRIX_COLS = 27

POST_OPERATIVE_OUTPUT = LOG_PATH + "/post_operative.log"

# Auto mpg dataset

AUTO_MPG_PATH = TMP_PATH + "/auto_mpg.data"
AUTO_MPG_HAS_HEADER = False
AUTO_MPG_DATA_TYPES = [NUM_RES, NUM, NUM, NUM, NUM, NUM, NUM, CAT, CAT]
AUTO_MPG_IS_CLASSIFY = False
AUTO_MPG_N_DATA_MATRIX_COLS = 317

AUTO_MPG_OUTPUT = LOG_PATH + "/auto_mpg.log"
