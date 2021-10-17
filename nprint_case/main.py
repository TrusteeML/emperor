import graphviz
import numpy as np

from sklearn import tree
from sklearn.metrics import classification_report
from sklearn.model_selection import train_test_split

from skexplain.utils import log
from skexplain.imitation import ClassificationDagger

from autogluon.tabular import TabularPredictor
from nprintml.label.aggregator import registry as aggregators


OUTPUT_DIR = "res/output/"

AGGREGATOR = "index"
LABELS_PATH = "res/dataset/single-pcap/labels.txt"
MODELS_DIR = "res/dataset/single-pcap/nprintml/model"
NPRINT_PATH = "res/dataset/single-pcap/nprintml/nprint/test.npt"

# AGGREGATOR = "pcap"
# LABELS_PATH = "res/dataset/multi-pcaps/labels.txt"
# MODELS_DIR = "res/dataset/multi-pcaps/nprintml/model"
# NPRINT_PATH = "res/dataset/multi-pcaps/nprintml/nprint"


def main():
    logger = log.Logger("{}/output.log".format(OUTPUT_DIR))
    logger.log("Reading nPrint dataset...")

    aggr = aggregators[AGGREGATOR](LABELS_PATH)
    df = aggr(NPRINT_PATH)

    y = df["label"]
    X = df.drop(labels=["label"], axis=1)

    X_indexes = np.arange(0, X.shape[0])
    X_train, X_test, y_train, y_test = train_test_split(X_indexes, y, train_size=0.7)
    X_train = X.iloc[X_train]
    X_test = X.iloc[X_test]
    logger.log("Done!")

    logger.log("Loading nPrintML model...")
    blackbox = TabularPredictor.load(MODELS_DIR, verbosity=1)
    logger.log("Done!")

    y_pred = blackbox.predict(X_test)
    logger.log("Blackbox model classification report with IID:")
    logger.log("\n{}".format(classification_report(y_test, y_pred, digits=3)))

    # Decision tree extraction
    logger.log("Using Classification Dagger algorithm to extract DT...")
    dagger = ClassificationDagger(expert=blackbox)

    dagger.fit(
        X_train,
        y_train,
        max_iter=100,
        max_leaf_nodes=None,
        num_samples=100,
        # samples_size=0.01,
        # ccp_alpha=0.00000001,
        verbose=True,
    )

    logger.log("#" * 10, "Explanation validation", "#" * 10)
    (dt, reward, idx) = dagger.explain()

    logger.log("Model explanation {} local fidelity: {}".format(idx, reward))
    dt_y_pred = dt.predict(X_test)

    logger.log("Model explanation global fidelity report:")
    logger.log(
        "\n{}".format(
            classification_report(
                y_pred,
                dt_y_pred,
                digits=3,
            )
        )
    )

    logger.log("Model explanation classification report:")
    logger.log(
        "\n{}".format(
            classification_report(
                y_test,
                dt_y_pred,
                digits=3,
            )
        )
    )

    dot_data = tree.export_graphviz(
        dt,
        class_names=y.unique(),
        feature_names=X.columns,
        filled=True,
        rounded=True,
        special_characters=True,
    )
    graph = graphviz.Source(dot_data)
    graph.render("{}/dt_{}_{}_{}".format(OUTPUT_DIR, "TabularPredictor", "dagger", dt.get_n_leaves()))


if __name__ == "__main__":
    main()
