import os
from sklearn.metrics import classification_report

from skexplain.utils import log

from skexplain.report import TrustReport

from autogluon.tabular import TabularPredictor
from nprintml.label.aggregator import registry as aggregators


AGGREGATOR = "pcap"
LABELS_PATH = "res/dataset/labels.txt"
MODELS_DIR = "res/dataset/nprintml/model"
NPRINT_PATH = "res/dataset/nprintml/nprint"
OUTPUT_PATH = "res/output"
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
        blackbox = TabularPredictor.load(MODELS_DIR, verbosity=1)
        logger.log("Done!")

        y_pred = blackbox.predict(X)
        logger.log("Blackbox model classification report with IID:")
        logger.log("\n{}".format(classification_report(y, y_pred, digits=3)))

        trust_report = TrustReport(
            blackbox,
            X=X,
            y=y,
            top_k=10,
            max_iter=10,
            trustee_num_iter=10,
            num_quantiles=20,
            skip_retrain=True,
            trustee_sample_size=0.3,
            class_names=sorted(y.unique()),
            feature_names=X.columns,
        )

    logger.log(trust_report)
    trust_report.plot(f"{OUTPUT_PATH}/report", aggregate=True)
    trust_report.save(OUTPUT_PATH)


if __name__ == "__main__":
    main()
