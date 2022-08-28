import os
import numpy as np

from trustee.utils import log
from trustee.report.trust import TrustReport
from autogluon.tabular import TabularPredictor
from nprintml.label.aggregator import registry as aggregators


# We want to fit the trustee and visualize the resulting decision tree of our full dataset using the model trained on tcp options only
# therefore the labels and nprint path should point to full dataset and model path should point to tcpoptions_only model
AGGREGATOR = "pcap"
LABELS_PATH = "res/nprint_tcp_options_dataset/labels.txt"  # labels file
# LABELS_PATH = "res/nprint_tcp_options_dataset/sub_labels.txt"  # labels file
# *.npt folder, result of pcap->npt parsing (usually nprint folder of output dir of nprintml)
NPRINT_PATH = "res/nprint_tcp_options_dataset/nprintml/nprint"
# NPRINT_PATH = "res/nprint_tcp_options_dataset/nprintml/sub_nprint"
# model folder, usually 'model' folder of output_dir of nprintml
MODELS_PATH = "res/nprint_tcp_options_dataset/nprintml/model"
OUTPUT_PATH = "res/output/tcpoptions_only_model"
REPORT_PATH = f"{OUTPUT_PATH}/report/trust_report.obj"


def main():
    logger = log.Logger("{}/output.log".format(OUTPUT_PATH))
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
            max_iter=1,
            trustee_num_iter=1,
            num_quantiles=20,
            # skip_retrain=True,
            trustee_sample_size=0.3,
            skip_retrain=True,
            class_names=sorted(y.unique()),  # [1:] to remove Kali linux instance
            feature_names=X.columns,
        )

    logger.log(trust_report)
    # trust_report.plot(f"{OUTPUT_PATH}/report", aggregate=True)
    trust_report.save(OUTPUT_PATH)


if __name__ == "__main__":
    main()
