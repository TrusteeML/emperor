# Reproducibility of DeepTraffic shortcut learning
import os
import numpy as np
import input_data
import graphviz


from sklearn import tree

from sklearn.metrics import classification_report

from trustee.utils import log
from trustee.report.trust import TrustReport

from deeptraffic import DeepTraffic

DATA_DIR = "res/dataset/train_test/2class/SessionAllLayers"
MODEL_DIR = os.path.split(DATA_DIR)[1]

VALIDATION_DATA_DIR = "res/dataset/validation/2class/SessionAllLayers"

CLASS_NUM = 2
dict_2class = {0: "Novpn", 1: "Vpn"}

OUTPUT_PATH = "res/output"
REPORT_PATH = f"{OUTPUT_PATH}/report/trust_report.obj"


def main():
    logger = log.Logger(f"{OUTPUT_PATH}/output.log")
    if os.path.exists(REPORT_PATH):
        logger.log(f"Loading trust report from {REPORT_PATH}...")
        trust_report = TrustReport.load(REPORT_PATH)
        logger.log("Done!")
    else:
        logger.log("DeepTraffic Validation Script Start")
        dataset = input_data.read_data_sets(DATA_DIR, one_hot=True, num_classes=CLASS_NUM)

        class_names = dict_2class.values()
        logger.log("Initializing DeepTraffic")
        deep_traffic = DeepTraffic()
        deep_traffic.fit(dataset.train, model_dir=MODEL_DIR)
        X_train = dataset.train.images
        y_train = np.array([np.argmax(i) for i in dataset.train.labels])
        X_test = dataset.test.images
        y_test = np.array([np.argmax(i) for i in dataset.test.labels])

        logger.log("Testing DeepTraffic")
        y_pred = deep_traffic.predict(X_test)

        logger.log("{}".format(classification_report(y_test, y_pred, digits=3, target_names=class_names)))

        trust_report = TrustReport(
            deep_traffic,
            X_train=X_train,
            X_test=X_test,
            y_train=y_train,
            y_test=y_test,
            top_k=10,
            max_iter=0,
            trustee_num_iter=10,
            num_pruning_iter=30,
            trustee_sample_size=0.3,
            analyze_stability=True,
            analyze_branches=True,
            skip_retrain=True,
            class_names=list(class_names),
            logger=logger,
            verbose=False,
        )
        deep_traffic.sess.close()

    trust_report.save(OUTPUT_PATH)
    logger.log(trust_report)


if __name__ == "__main__":
    main()
