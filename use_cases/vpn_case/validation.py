# Reproducibility of DeepTraffic shortcut learning
import os
import numpy as np
import input_data

from sklearn.metrics import classification_report

from trustee.utils import log

from deeptraffic import DeepTraffic

DATA_DIR = "res/dataset/train_test/2class/SessionAllLayers"
MODEL_DIR = os.path.split(DATA_DIR)[1]

VALIDATION_DATA_DIR = "res/dataset/validation/2class/SessionAllLayers"
VALIDATION_64_DATA_DIR = "res/dataset/validation/2class-64/SessionAllLayers"  # altered first 64 bytes
VALIDATION_128_DATA_DIR = "res/dataset/validation/2class-128/SessionAllLayers"  # altered first 128 bytes
VALIDATION_32_64_DATA_DIR = "res/dataset/validation/2class-32-64/SessionAllLayers"  # altered from 32nd to 64th byte
VALIDATION_43_47_49_DATA_DIR = "res/dataset/validation/2class-43-47-49/SessionAllLayers"  # altered bytes 43 47 49

CLASS_NUM = 2
dict_2class = {0: "Novpn", 1: "Vpn"}

OUTPUT_PATH = "res/output"
REPORT_PATH = f"{OUTPUT_PATH}/report/trust_report.obj"


def main():
    logger = log.Logger(f"{OUTPUT_PATH}/output.log")

    logger.log("DeepTraffic Validation Script Start")
    dataset = input_data.read_data_sets(DATA_DIR, one_hot=True, num_classes=CLASS_NUM)

    print(type(dataset))

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

    # Untempered dataset validation
    logger.log("Validating DeepTraffic")
    validation_dataset = input_data.read_data_sets(VALIDATION_DATA_DIR, one_hot=True, num_classes=CLASS_NUM)

    X_validation = validation_dataset.test.images
    y_validation = np.array([np.argmax(i) for i in validation_dataset.test.labels])
    y_val_pred = deep_traffic.predict(X_validation)

    logger.log("Untampered dataset classification report")
    logger.log("{}".format(classification_report(y_validation, y_val_pred, digits=3, target_names=class_names)))

    # Tempered dataset validation (bytes 43, 47 and 49)
    alt_43_47_49_dataset = input_data.read_data_sets(VALIDATION_43_47_49_DATA_DIR, one_hot=True, num_classes=CLASS_NUM)

    X_validation_alt_43_47_49 = alt_43_47_49_dataset.test.images
    y_validation_alt_43_47_49 = np.array([np.argmax(i) for i in alt_43_47_49_dataset.test.labels])
    y_val_alt_43_47_49_pred = deep_traffic.predict(X_validation_alt_43_47_49)

    logger.log("Tempered dataset bytes 43, 47 and 49 classification report")
    logger.log(
        "{}".format(
            classification_report(
                y_validation_alt_43_47_49,
                y_val_alt_43_47_49_pred,
                digits=3,
                target_names=class_names,
            )
        )
    )

    # Tempered dataset validation (bytes 32-64)
    alt_32_64_dataset = input_data.read_data_sets(VALIDATION_32_64_DATA_DIR, one_hot=True, num_classes=CLASS_NUM)

    X_validation_alt_32_64 = alt_32_64_dataset.test.images
    y_validation_alt_32_64 = np.array([np.argmax(i) for i in alt_32_64_dataset.test.labels])
    y_val_alt_32_64_pred = deep_traffic.predict(X_validation_alt_32_64)

    logger.log("Tempered dataset bytes 32-64 classification report")
    logger.log(
        "{}".format(
            classification_report(
                y_validation_alt_32_64,
                y_val_alt_32_64_pred,
                digits=3,
                target_names=class_names,
            )
        )
    )

    # Tempered dataset validation (bytes 0-64)
    alt_64_dataset = input_data.read_data_sets(VALIDATION_64_DATA_DIR, one_hot=True, num_classes=CLASS_NUM)

    X_validation_alt_64 = alt_64_dataset.test.images
    y_validation_alt_64 = np.array([np.argmax(i) for i in alt_64_dataset.test.labels])
    y_val_alt_64_pred = deep_traffic.predict(X_validation_alt_64)

    logger.log("Tempered dataset bytes 0-64 classification report")
    logger.log(
        "{}".format(
            classification_report(
                y_validation_alt_64,
                y_val_alt_64_pred,
                digits=3,
                target_names=class_names,
            )
        )
    )

    # Tempered dataset validation (bytes 0-128)
    alt_128_dataset = input_data.read_data_sets(VALIDATION_128_DATA_DIR, one_hot=True, num_classes=CLASS_NUM)

    X_validation_alt_128 = alt_128_dataset.test.images
    y_validation_alt_128 = np.array([np.argmax(i) for i in alt_128_dataset.test.labels])
    y_val_alt_128_pred = deep_traffic.predict(X_validation_alt_128)

    logger.log("Tempered dataset bytes 0-128 classification report")
    logger.log(
        "{}".format(
            classification_report(
                y_validation_alt_128,
                y_val_alt_128_pred,
                digits=3,
                target_names=class_names,
            )
        )
    )


if __name__ == "__main__":
    main()
