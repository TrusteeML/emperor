import os

from trustee.report import TrustReport
from trustee.utils import dataset, log
from trustee.utils.const import IOT_DATASET_META

from sklearn.ensemble import RandomForestClassifier


OUTPUT_PATH = "res/output"
DF_DATASET_PATH = "res/dataset/zip_files/16-09-23-labeled.csv.zip"
IOT_DATASET_META["is_dir"] = False

REPORT_PATH = f"{OUTPUT_PATH}/report/trust_report.obj"


def main():
    """Test using Reinforcement Learning to extract Decision Tree from a generic Blackbox model"""
    logger = log.Logger(f"{OUTPUT_PATH}/output.log")

    if os.path.exists(REPORT_PATH):
        logger.log(f"Loading trust report from {REPORT_PATH}...")
        trust_report = TrustReport.load(REPORT_PATH)
        logger.log("Done!")
    else:
        # Step 1: Load training dataset
        logger.log("Reading dataset from CSV...")
        X, y, feature_names, _, _ = dataset.read(
            DF_DATASET_PATH,
            metadata=IOT_DATASET_META,
            verbose=False,
            logger=logger,
            as_df=True,
        )
        logger.log("Done!")

        blackbox = RandomForestClassifier(n_jobs=4)
        trust_report = TrustReport(
            blackbox,
            X=X,
            y=y,
            logger=logger,
            top_k=1,
            max_iter=1,
            num_pruning_iter=1,
            trustee_num_iter=1,
            feature_names=feature_names,
            class_names=IOT_DATASET_META["classes"],
            verbose=True,
        )

    logger.log(trust_report)
    trust_report.save(OUTPUT_PATH)


if __name__ == "__main__":
    main()
