import os
import graphviz

from sklearn import tree

from trustee.utils import log
from trustee.report import TrustReport

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

    stable_explanations = trust_report.get_stable_explanations()
    stability_output_dir = f"{OUTPUT_PATH}/stable"
    if not os.path.exists(stability_output_dir):
        os.makedirs(stability_output_dir)

    logger.log("Saving stability decision trees...")
    for idx, it in enumerate(stable_explanations):
        print(it)
        dot_data = tree.export_graphviz(
            it["dt"],
            class_names=sorted(trust_report.y.unique()),
            feature_names=trust_report.feature_names,
            filled=True,
            rounded=True,
            special_characters=True,
        )
        graph = graphviz.Source(dot_data)
        graph.render(f"{stability_output_dir}/dt_{idx}")

    logger.log(trust_report)
    trust_report.save(OUTPUT_PATH)


if __name__ == "__main__":
    main()
