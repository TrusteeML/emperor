import os
import numpy as np

from skexplain.report import TrustReport
from skexplain.utils import dataset, log, persist
from skexplain.utils.const import CIC_IDS_2017_DATASET_META

from sklearn.ensemble import RandomForestClassifier
from sklearn.model_selection import train_test_split


DF_PATH = "res/dataset/CIC-IDS-2017/"
DF_OVER_PATH = "res/dataset/CIC-IDS-2017_OverSampled.csv.zip"
DF_OVER_MIN_PATH = "res/dataset/CIC-IDS-2017_OverSampled_min.csv.zip"
MODEL_PATH = "res/models/RandomForestClassifier_cic_ids_2017.joblib.zip"

OUTPUT_PATH = "res/output"
REPORT_PATH = f"{OUTPUT_PATH}/report/trust_report.obj"

# if using oversampled df
CIC_IDS_2017_DATASET_META["is_dir"] = False


def main():
    logger = log.Logger("{}/output.log".format(OUTPUT_PATH))

    if os.path.exists(REPORT_PATH):
        logger.log(f"Loading trust report from {REPORT_PATH}...")
        trust_report = TrustReport.load(REPORT_PATH)
        logger.log("Done!")
    else:
        logger.log("Reading CIC-IDS-2017 dataset...")
        # Step 1: Parse train-test def
        X, y, feature_names, _, _ = dataset.read(
            DF_OVER_MIN_PATH, metadata=CIC_IDS_2017_DATASET_META, as_df=True, verbose=True
        )
        logger.log("Done!")

        blackbox = RandomForestClassifier(n_jobs=4)
        trust_report = TrustReport(
            blackbox,
            X=X,
            y=y,
            logger=logger,
            top_k=20,
            max_iter=10,
            trustee_num_iter=30,
            num_pruning_iter=10,
            trustee_sample_size=0.3,
            feature_names=feature_names,
            class_names=CIC_IDS_2017_DATASET_META["classes"],
            verbose=True,
        )

    logger.log(trust_report)
    trust_report.save(OUTPUT_PATH)


if __name__ == "__main__":
    main()
