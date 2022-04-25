import graphviz
import pickle

from sklearn import tree
from sklearn.metrics import classification_report, confusion_matrix

from skexplain.utils import log
from skexplain.imitation import ClassificationDagger

from autogluon.tabular import TabularPredictor
from nprintml.label.aggregator import registry as aggregators


# Now we want to load the model trained on the full dataset and apply to campus dataset
# therefore labels and nprint path should be for campus dataset and model dir should be for full model folder
AGGREGATOR = "pcap"
LABELS_PATH = "res/campus_dataset/labels.txt"
NPRINT_PATH = "res/campus_dataset/npts"
MODELS_DIR = "res/nprint_dataset/full_model/model"
OUTPUT_DIR = "results/full_model"


def main():
    logger = log.Logger("{}/output.log".format(OUTPUT_DIR))
    logger.log("Reading nPrint dataset...")

    labels = list(sorted(["benign_benign", "malware_ddos", "malware_dos", "malware_ftp-patator", "malware_infiltration", "malware_port-scan", "malware_ssh-patator", "malware_web-attack"]))
    aggr = aggregators[AGGREGATOR](LABELS_PATH)
    df = aggr(NPRINT_PATH)

    y = df["label"]
    X = df.drop(labels=["label"], axis=1)

    logger.log("X size: {}; y size: {}".format(len(X), len(y)))
    logger.log("Done!")

    logger.log("Loading nPrintML model...")
    blackbox = TabularPredictor.load(MODELS_DIR, verbosity=1)
    logger.log("Done!")

    y_pred = blackbox.predict(X)
    logger.log("Blackbox model classification report with IID:")
    logger.log("\n{}".format(classification_report(y, y_pred, digits=3)))

    logger.log("Full confusion matrix: ")
    logger.log(confusion_matrix(y, y_pred, labels=labels))

    # Decision tree extraction
    logger.log("Using Classification Dagger algorithm to extract DT...")
    dagger = ClassificationDagger(expert=blackbox)

    dagger.fit(X, y, num_iter=40, samples_size=1.0, verbose=True)

    logger.log("#" * 10, "Explanation validation", "#" * 10)
    (dt, reward, idx) = dagger.explain()

    logger.log("Model explanation {} local fidelity: {}".format(idx, reward))
    dt_y_pred = dt.predict(X)

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
                y,
                dt_y_pred,
                digits=3,
            )
        )
    )

    with open(f"{OUTPUT_DIR}/dt.pkl", "wb") as f:
        pickle.dump(dt, f)

    dot_data = tree.export_graphviz(
        dt,
        class_names=labels,
        feature_names=X.columns,
        filled=True,
        rounded=True,
        special_characters=True,
    )
    graph = graphviz.Source(dot_data)
    graph.render("{}/dt_{}_{}_{}".format(OUTPUT_DIR, "TabularPredictor", "dagger", dt.get_n_leaves()))


if __name__ == "__main__":
    main()
