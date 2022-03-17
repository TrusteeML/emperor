import graphviz
import numpy as np

from sklearn import tree
from sklearn.metrics import classification_report
from sklearn.model_selection import train_test_split

from skexplain.utils import log
from skexplain.imitation import ClassificationDagger
from skexplain.report import trust_report

from autogluon.tabular import TabularPredictor
from nprintml.label.aggregator import registry as aggregators

# AGGREGATOR = "index"
# LABELS_PATH = "res/dataset/single-pcap/labels.txt"
# MODELS_DIR = "res/dataset/single-pcap/nprintml/model"
# NPRINT_PATH = "res/dataset/single-pcap/nprintml/nprint/test.npt"
# OUTPUT_DIR = "res/output/single-pcap/"


# AGGREGATOR = "pcap"
# LABELS_PATH = "res/dataset/multi-pcaps/labels.txt"
# MODELS_DIR = "res/dataset/multi-pcaps/nprintml/model"
# NPRINT_PATH = "res/dataset/multi-pcaps/nprintml/nprint"
# OUTPUT_DIR = "res/output/multi-pcap/"


AGGREGATOR = "pcap"
LABELS_PATH = "res/dataset/os-fingerprint/labels.txt"
MODELS_DIR = "res/dataset/os-fingerprint/nprintml/model"
NPRINT_PATH = "res/dataset/os-fingerprint/nprintml/nprint"
OUTPUT_DIR = "res/output/os-fingerprint/"


def main():
    logger = log.Logger("{}/output.log".format(OUTPUT_DIR))
    logger.log("Reading nPrint dataset...")

    aggr = aggregators[AGGREGATOR](LABELS_PATH)
    df = aggr(NPRINT_PATH)

    y = df["label"]
    X = df.drop(labels=["label"], axis=1)

    logger.log("Loading nPrintML model...")
    blackbox = TabularPredictor.load(MODELS_DIR, verbosity=1)
    logger.log("Done!")

    y_pred = blackbox.predict(X_test)
    logger.log("Blackbox model classification report with IID:")
    logger.log("\n{}".format(classification_report(y_test, y_pred, digits=3)))

    logger.log(
        trust_report(
            blackbox,
            X=X,
            y=y,
            skip_retrain=True,
            output_dir=OUTPUT_DIR,
            class_names=sorted(y.unique()),  # [1:] to remove Kali linux instance
            feature_names=X.columns,
        )
    )


if __name__ == "__main__":
    main()
