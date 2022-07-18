import os

from skexplain.utils import log
from skexplain.report import TrustReport

from autogluon.tabular import TabularPredictor
from nprintml.label.aggregator import registry as aggregators


AGGREGATOR = "pcap"
# LABELS_PATH = "res/nprint_dataset/sub_labels.txt"
LABELS_PATH = "res/nprint_dataset/labels.txt"
MODELS_PATH = "res/nprint_dataset/full_model/model"
# NPRINT_PATH = "res/nprint_dataset/full_model/nprint"
NPRINT_PATH = "res/nprint_dataset/nprintml/sub_nprint"
OUTPUT_PATH = "results/full_model/"
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
            top_k=20,
            max_iter=100,
            trustee_num_iter=100,
            num_quantiles=0,
            trustee_sample_size=0.3,
            skip_retrain=True,
            class_names=sorted(y.unique()),  # [1:] to remove Kali linux instance
            feature_names=X.columns,
        )
    logger.log(trust_report)
    trust_report.plot(f"{OUTPUT_PATH}/report", aggregate=True)
    trust_report.save(OUTPUT_PATH)


if __name__ == "__main__":
    main()
