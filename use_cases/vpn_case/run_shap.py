# Reproducibility of DeepTraffic shortcut learning
import os
import numpy as np

import shap

from sklearn import tree
from sklearn.metrics import classification_report

from trustee.utils import log

import input_data
from deeptraffic import DeepTraffic

DATA_DIR = "res/dataset/train_test/2class/SessionAllLayers"
MODEL_DIR = os.path.split(DATA_DIR)[1]

VALIDATION_DATA_DIR = "res/dataset/validation/2class/SessionAllLayers"

CLASS_NUM = 2
dict_2class = {0: "Novpn", 1: "Vpn"}


def main():
    logger = log.Logger("res/output/output.log")

    logger.log("DeepTraffic Validation Script Start")
    dataset = input_data.read_data_sets(DATA_DIR, one_hot=True, num_classes=CLASS_NUM)

    class_names = dict_2class.values()
    logger.log("Initializing DeepTraffic")
    deep_traffic = DeepTraffic()
    deep_traffic.fit(dataset.train, model_dir=MODEL_DIR)
    X_train = dataset.train.images
    # y_train = np.array([np.argmax(i) for i in dataset.train.labels])
    X_test = dataset.test.images
    y_test = np.array([np.argmax(i) for i in dataset.test.labels])

    logger.log("Testing DeepTraffic")
    y_pred = deep_traffic.predict(X_test)

    logger.log("{}".format(classification_report(y_test, y_pred, digits=3, target_names=class_names)))

    # Untempered dataset validation
    logger.log("Validating DeepTraffic")
    validation_dataset = input_data.read_data_sets(VALIDATION_DATA_DIR, one_hot=True, num_classes=CLASS_NUM)

    X_validation = validation_dataset.test.images
    y_validation = np.array([np.argmax(i) for i in validation_dataset.test.labels])
    y_val_pred = deep_traffic.predict(X_validation)

    logger.log("Untampered dataset classification report")
    logger.log("{}".format(classification_report(y_validation, y_val_pred, digits=3, target_names=class_names)))

    # load JS visualization code to notebook
    shap.initjs()
    background = X_train[np.random.choice(X_train.shape[0], 100, replace=False)]

    # explain the model's predictions using SHAP
    explainer = shap.KernelExplainer(deep_traffic.predict_proba, background, link="identity")
    X_test_samples = X_test[np.random.choice(X_test.shape[0], 100, replace=False)]
    logger.log("SHAP Test samples:", X_test_samples.shape[0])
    shap_values = explainer.shap_values(X_test_samples, nsamples=100)

    # summarize the effects of all the features
    shap.summary_plot(shap_values, X_test_samples)
    # shap.dependence_plot(23, shap_values[0], X_test_samples)

    # for cls in range(len(dataset_meta["classes"])):
    # shap.summary_plot(shap_values[cls], X_test, plot_type="bar", feature_names=feature_names)


if __name__ == "__main__":
    main()
