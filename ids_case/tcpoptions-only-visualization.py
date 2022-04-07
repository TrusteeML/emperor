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


# We want to fit the dagger and visualize the resulting decision tree of our full dataset using the model trained on tcp options only
# therefore the labels and nprint path should point to full dataset and model path should point to tcpoptions_only model
AGGREGATOR = "pcap"
LABELS_PATH = "res/nprint_dataset/labels.txt"   # labels file
NPRINT_PATH = "res/nprint_dataset/tcpoptions_only_model/nprint"  # *.npt folder, result of pcap->npt parsing (usually nprint folder of output dir of nprintml)
MODELS_DIR = "res/nprint_dataset/tcpoptions_only_model/model"  # model folder, usually 'model' folder of output_dir of nprintml
OUTPUT_DIR = "results/tcpoptions_only_model"


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
    logger.log("X size: {}; y size: {}".format(len(X), len(y)))
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
        num_iter=100,
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
        class_names=sorted(y.unique()),
        feature_names=X.columns,
        filled=True,
        rounded=True,
        special_characters=True,
    )
    graph = graphviz.Source(dot_data)
    graph.render("{}/dt_{}_{}_{}".format(OUTPUT_DIR, "TabularPredictor", "dagger", dt.get_n_leaves()))

    logger.log(
        trust_report(
            blackbox,
            X=X,
            y=y,
            skip_retrain=True,
            output_dir=OUTPUT_DIR,
            class_names=sorted(y.unique()),
            feature_names=X.columns,
        )
    )


if __name__ == "__main__":
    main()
