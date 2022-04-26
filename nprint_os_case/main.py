import os
import graphviz
import numpy as np

from sklearn import tree
from sklearn.metrics import classification_report
from sklearn.model_selection import train_test_split

from skexplain.utils import log

# from skexplain.imitation import ClassificationTrustee
# from skexplain.report import TrustReport

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
        # trust_report = TrustReport.load(REPORT_PATH)
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

        df_alt_ttl = df.groupby("label").get_group(" Linux 3.11 and newer")
        df_alt_ttl = df_alt_ttl.assign(
            # TTL = 62
            ipv4_ttl_0=0,
            ipv4_ttl_1=0,
            ipv4_ttl_2=1,
            ipv4_ttl_3=1,
            ipv4_ttl_4=1,
            ipv4_ttl_5=1,
            ipv4_ttl_6=1,
            ipv4_ttl_7=0,
            # Window Size = 5000
            tcp_wsize_0=0,
            tcp_wsize_1=0,
            tcp_wsize_2=0,
            tcp_wsize_3=1,
            tcp_wsize_4=0,
            tcp_wsize_5=0,
            tcp_wsize_6=1,
            tcp_wsize_7=1,
            tcp_wsize_8=1,
            tcp_wsize_9=0,
            tcp_wsize_10=0,
            tcp_wsize_11=0,
            tcp_wsize_12=1,
            tcp_wsize_13=0,
            tcp_wsize_14=0,
            tcp_wsize_15=0,
            # TCP OPTIONS 32 bits = 0
            tcp_opt_0=1,
            tcp_opt_1=1,
            tcp_opt_2=1,
            tcp_opt_3=1,
            tcp_opt_4=1,
            tcp_opt_5=1,
            tcp_opt_6=1,
            tcp_opt_7=1,
            tcp_opt_8=1,
            tcp_opt_9=1,
            tcp_opt_10=1,
            tcp_opt_11=1,
            tcp_opt_12=1,
            tcp_opt_13=1,
            tcp_opt_14=1,
            tcp_opt_15=1,
            tcp_opt_16=1,
            tcp_opt_17=1,
            tcp_opt_18=1,
            tcp_opt_19=1,
            tcp_opt_20=1,
            tcp_opt_21=1,
            tcp_opt_22=1,
            tcp_opt_23=1,
            tcp_opt_24=1,
            tcp_opt_25=1,
            tcp_opt_26=1,
            tcp_opt_27=1,
            tcp_opt_28=1,
            tcp_opt_29=1,
            tcp_opt_30=1,
            tcp_opt_31=1,
            tcp_opt_32=1,
        )

        print(df_alt_ttl)

        y_alt = df_alt_ttl["label"]
        X_alt = df_alt_ttl.drop(labels=["label"], axis=1)

        y_pred_alt = blackbox.predict(X_alt)
        print(y_pred_alt)
        logger.log("Blackbox model classification report with OOD:")
        logger.log("\n{}".format(classification_report(y_alt, y_pred_alt, digits=3)))

    #     trust_report = TrustReport(
    #         blackbox,
    #         X=X,
    #         y=y,
    #         top_n=10,
    #         max_iter=1,
    #         trustee_num_iter=1,
    #         num_quantiles=20,
    #         # skip_retrain=True,
    #         trustee_sample_size=0.3,
    #         skip_retrain=True,
    #         class_names=sorted(y.unique()),  # [1:] to remove Kali linux instance
    #         feature_names=X.columns,
    #     )

    # logger.log(trust_report)
    # trust_report.plot(f"{OUTPUT_PATH}/report", aggregate=True)
    # trust_report.save(OUTPUT_PATH)


if __name__ == "__main__":
    main()
