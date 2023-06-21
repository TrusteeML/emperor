import os

from trustee.utils import log
from trustee.report.trust import TrustReport
from autogluon.tabular import TabularPredictor
from nprintml.label.aggregator import registry as aggregators


AGGREGATOR = "pcap"
# LABELS_PATH = "res/nprint_dataset/sub_labels.txt"
LABELS_PATH = "res/nprint_dataset/labels.txt"
MODELS_PATH = "res/nprint_dataset/nprintml/model"
NPRINT_PATH = "res/nprint_dataset/nprintml/nprint"
# NPRINT_PATH = "res/nprint_dataset/nprintml/sub_nprint"
OUTPUT_PATH = "res/output/full_model/"
REPORT_PATH = f"{OUTPUT_PATH}/report/trust_report.obj"


def main():
    logger = log.Logger(f"{OUTPUT_PATH}/output.log")
    if os.path.exists(REPORT_PATH):
        logger.log("Loading trust report from {}...".format(REPORT_PATH))
        trust_report = TrustReport.load(REPORT_PATH)
        logger.log("Done!")
    else:
        logger.log("Reading nPrint dataset...")

        aggr = aggregators[AGGREGATOR](LABELS_PATH)
        df = aggr(NPRINT_PATH)

        y = df["label"]
        X = df.drop(labels=["label"], axis=1)

        logger.log("Loading nPrintML model...")
        blackbox = TabularPredictor.load(MODELS_PATH, verbosity=1)
        logger.log("Done!")

        trust_report = TrustReport(
            blackbox,
            X=X,
            y=y,
            top_k=10,
            max_iter=50,
            trustee_num_iter=10,
            num_pruning_iter=0,
            skip_retrain=True,
            analyze_stability=True,
            trustee_sample_size=0.3,
            class_names=sorted(y.unique()),
            feature_names=X.columns,
            verbose=True,
        )

    logger.log(trust_report)
    trust_report.save(OUTPUT_PATH)


if __name__ == "__main__":
    main()
