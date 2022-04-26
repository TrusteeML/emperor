import os
import numpy as np
import pandas as pd

from skexplain.report import TrustReport
from skexplain.utils import dataset, log, persist
from skexplain.utils.const import CIC_IDS_2017_DATASET_META

from sklearn.ensemble import RandomForestClassifier
from sklearn.metrics import classification_report
from sklearn.model_selection import train_test_split


DF_TRAIN_TEST_PATH = "res/dataset/CIC-IDS-2017/"
DF_TRAIN_TEST_OVER_PATH = "res/dataset/CIC-IDS-2017_OverSampled.csv.zip"
DF_VALIDATE_PATH = "res/dataset/validation/heartbleed.csv"
MODEL_PATH = "RandomForestClassifier_cic_ids_2017.joblib.zip"

OUTPUT_PATH = "res/output"
REPORT_PATH = f"{OUTPUT_PATH}/report/trust_report.obj"

# if using oversampled df
CIC_IDS_2017_DATASET_META["is_dir"] = False


def main():
    print("Reading dataset...")
    df = pd.read_csv(DF_TRAIN_TEST_OVER_PATH)
    y = df["Label"]
    X = df.drop(["Label"], axis=1)

    print("Splitting dataset...")
    X_indexes = np.arange(0, X.shape[0])
    X_train, _, y_train, _ = train_test_split(X_indexes, y, train_size=0.01, stratify=y)
    X_train = X.iloc[X_train]

    print(X_train)

    df = X_train
    df["Label"] = y_train

    print("Saving dataset...")
    df.to_csv(
        "res/dataset/CIC-IDS-2017_OverSampled_min.csv.zip",
        sep=",",
        header=True,
        index=False,
        chunksize=100000,
        compression="zip",
        encoding="utf-8",
    )


if __name__ == "__main__":
    main()
