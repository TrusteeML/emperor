import os
import csv
import graphviz
import scipy.stats
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt

from sklearn import tree
from sklearn.metrics import f1_score, classification_report
from sklearn.model_selection import train_test_split


from skexplain.imitation import ClassificationTrustee
from skexplain.utils import log, input_data

from deeptraffic import DeepTraffic

OUTPUT_PATH = "res/output"
DATA_DIR = "res/dataset/train_test/2class/SessionAllLayers"
MODEL_DIR = os.path.split(DATA_DIR)[1]

VALIDATION_DATA_DIR = "res/dataset/validation/2class/SessionAllLayers"
VALIDATION_64_DATA_DIR = "res/dataset/validation/2class-64/SessionAllLayers"  # altered first 64 bytes
VALIDATION_128_DATA_DIR = "res/dataset/validation/2class-128/SessionAllLayers"  # altered first 128 bytes
VALIDATION_32_64_DATA_DIR = "res/dataset/validation/2class-32-64/SessionAllLayers"  # altered from 32nd to 64th byte
VALIDATION_43_47_49_DATA_DIR = "res/dataset/validation/2class-43-47-49/SessionAllLayers"  # altered bytes 43 47 49

CLASS_NUM = 2
dict_2class = {0: "Novpn", 1: "Vpn"}


def main():
    logger = log.Logger(f"{OUTPUT_PATH}/output.log")

    logger.log("DeepTraffic Validation Script Start")
    dataset = input_data.read_data_sets(DATA_DIR, one_hot=True, num_classes=CLASS_NUM)

    class_names = list(dict_2class.values())
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

    output_dir = f"{OUTPUT_PATH}/ablation"
    if not os.path.exists(output_dir):
        os.makedirs(output_dir)

    num_iter = 50
    train_size = 0.7
    with open(f"{output_dir}/ablation.csv", "w") as f:
        # create the csv writer
        writer = csv.writer(f)
        writer.writerow(
            [
                "iteration",
                "samples size",
                "method",
                "dt_size",
                "fidelity_macro",
                "accuracy_macro",
                "fidelity_weighted",
                "accuracy_weighted",
            ]
        )

        for samples_size in np.arange(0.05, 0.55, 0.05):
            for i in range(30):
                #####################################
                ############# STRAWMAN ##############
                #####################################

                size = int(int(len(X_train)) * 0.001)
                samples_idxs = np.random.choice(len(X_train), size=size, replace=False)
                X_iter, y_iter = X_train[samples_idxs], y_train[samples_idxs]

                X_sample_train, _, _, _ = train_test_split(X_iter, y_iter, train_size=train_size)
                y_pred_train = deep_traffic.predict(X_sample_train)

                dt = tree.DecisionTreeClassifier()
                dt = dt.fit(X_sample_train, y_pred_train)
                dt_y_pred = dt.predict(X_test)

                logger.log("Straw-man explanation global fidelity report:")
                logger.log("\n{}".format(classification_report(y_pred, dt_y_pred, digits=3)))

                logger.log("Straw-man explanation classification report:")
                logger.log("\n{}".format(classification_report(y_test, dt_y_pred, digits=3)))

                writer.writerow(
                    [
                        i,
                        samples_size,
                        "ablation",
                        dt.tree_.node_count,
                        f1_score(y_pred, dt_y_pred, average="macro"),
                        f1_score(y_test, dt_y_pred, average="macro"),
                        f1_score(y_pred, dt_y_pred, average="weighted"),
                        f1_score(y_test, dt_y_pred, average="weighted"),
                    ]
                )

                #######################################
                ######### NOtrustee + ACCURACY #########
                #######################################

                logger.log("Using Classification Trustee algorithm to extract DT...")
                trustee = ClassificationTrustee(expert=deep_traffic)

                trustee.fit(
                    X_train,
                    y_train,
                    num_iter=num_iter,
                    train_size=train_size,
                    samples_size=samples_size,
                    optimization="accuracy",
                    aggregate=False,
                    verbose=True,
                )

                logger.log("#" * 10, "Explanation validation", "#" * 10)
                (dt, reward, idx) = trustee.explain()

                logger.log("Accuracy-based  model explanation {} local fidelity: {}".format(idx, reward))
                dt_y_pred = dt.predict(X_test)

                logger.log("Accuracy-based model explanation w/o dataset aggregation global fidelity report:")
                logger.log("\n{}".format(classification_report(y_pred, dt_y_pred, digits=3)))

                logger.log("Accuracy-based model explanation w/o dataset aggregation classification report:")
                logger.log("\n{}".format(classification_report(y_test, dt_y_pred, digits=3)))

                writer.writerow(
                    [
                        i,
                        samples_size,
                        "no_trustee_accuracy",
                        dt.tree_.node_count,
                        f1_score(y_pred, dt_y_pred, average="macro"),
                        f1_score(y_test, dt_y_pred, average="macro"),
                        f1_score(y_pred, dt_y_pred, average="weighted"),
                        f1_score(y_test, dt_y_pred, average="weighted"),
                    ]
                )

                #######################################
                ######### NOtrustee + FIDELITY #########
                #######################################

                logger.log("Using Classification Trustee algorithm to extract DT...")
                trustee = ClassificationTrustee(expert=deep_traffic)

                trustee.fit(
                    X_train,
                    y_train,
                    num_iter=num_iter,
                    train_size=train_size,
                    samples_size=samples_size,
                    optimization="accuracy",
                    aggregate=False,
                    verbose=True,
                )

                logger.log("#" * 10, "Explanation validation", "#" * 10)
                (dt, reward, idx) = trustee.explain()

                logger.log("Accuracy-based  model explanation {} local fidelity: {}".format(idx, reward))
                dt_y_pred = dt.predict(X_test)

                logger.log("Accuracy-based model explanation w/o dataset aggregation global fidelity report:")
                logger.log("\n{}".format(classification_report(y_pred, dt_y_pred, digits=3)))

                logger.log("Accuracy-based model explanation w/o dataset aggregation classification report:")
                logger.log("\n{}".format(classification_report(y_test, dt_y_pred, digits=3)))

                writer.writerow(
                    [
                        i,
                        samples_size,
                        "no_trustee_fidelity",
                        dt.tree_.node_count,
                        f1_score(y_pred, dt_y_pred, average="macro"),
                        f1_score(y_test, dt_y_pred, average="macro"),
                        f1_score(y_pred, dt_y_pred, average="weighted"),
                        f1_score(y_test, dt_y_pred, average="weighted"),
                    ]
                )

                #####################################
                ######### trustee + ACCURACY #########
                #####################################

                logger.log("Using Classification Trustee algorithm to extract DT...")
                trustee = ClassificationTrustee(expert=deep_traffic)

                trustee.fit(
                    X_train,
                    y_train,
                    num_iter=num_iter,
                    train_size=train_size,
                    samples_size=samples_size,
                    optimization="accuracy",
                    verbose=True,
                )

                logger.log("#" * 10, "Explanation validation", "#" * 10)
                (dt, reward, idx) = trustee.explain()

                logger.log("Accuracy-based  model explanation {} local fidelity: {}".format(idx, reward))
                dt_y_pred = dt.predict(X_test)

                logger.log("Accuracy-based model explanation global fidelity report:")
                logger.log(
                    "\n{}".format(
                        classification_report(
                            y_pred,
                            dt_y_pred,
                            digits=3,
                        )
                    )
                )

                logger.log("Accuracy-based  model explanation classification report:")
                logger.log(
                    "\n{}".format(
                        classification_report(
                            y_test,
                            dt_y_pred,
                            digits=3,
                        )
                    )
                )

                writer.writerow(
                    [
                        i,
                        samples_size,
                        "trustee_accuracy",
                        dt.tree_.node_count,
                        f1_score(y_pred, dt_y_pred, average="macro"),
                        f1_score(y_test, dt_y_pred, average="macro"),
                        f1_score(y_pred, dt_y_pred, average="weighted"),
                        f1_score(y_test, dt_y_pred, average="weighted"),
                    ]
                )

                #####################################
                ######### trustee + FIDELITY #########
                #####################################

                logger.log("Using Classification Trustee algorithm to extract DT...")
                trustee = ClassificationTrustee(expert=deep_traffic)

                trustee.fit(
                    X_train,
                    y_train,
                    num_iter=num_iter,
                    train_size=train_size,
                    samples_size=samples_size,
                    verbose=True,
                )

                logger.log("#" * 10, "Explanation validation", "#" * 10)
                (dt, reward, idx) = trustee.explain()

                logger.log("Fidelity-based model explanation {} local fidelity: {}".format(idx, reward))
                dt_y_pred = dt.predict(X_test)

                logger.log("Fidelity-based Model explanation global fidelity report:")
                logger.log(
                    "\n{}".format(
                        classification_report(
                            y_pred,
                            dt_y_pred,
                            digits=3,
                        )
                    )
                )

                logger.log("Fidelity-based model explanation classification report:")
                logger.log(
                    "\n{}".format(
                        classification_report(
                            y_test,
                            dt_y_pred,
                            digits=3,
                        )
                    )
                )

                writer.writerow(
                    [
                        i,
                        samples_size,
                        "trustee_fidelity",
                        dt.tree_.node_count,
                        f1_score(y_pred, dt_y_pred, average="macro"),
                        f1_score(y_test, dt_y_pred, average="macro"),
                        f1_score(y_pred, dt_y_pred, average="weighted"),
                        f1_score(y_test, dt_y_pred, average="weighted"),
                    ]
                )

    deep_traffic.sess.close()


def mean_confidence_interval(data, confidence=0.95):
    a = 1.0 * np.array(data)
    n = len(a)
    m, se = np.mean(a), scipy.stats.sem(a)
    h = se * scipy.stats.t.ppf((1 + confidence) / 2.0, n - 1)
    return m, m - h, m + h


def plot_results():
    """Plots results of ablation approach comparison"""
    comparison = {
        "dt_size": {},
        "fidelity_macro": {},
        "accuracy_macro": {},
        "fidelity_weighted": {},
        "accuracy_weighted": {},
    }

    output_dir = f"{OUTPUT_PATH}/ablation"
    with open(f"{output_dir}/ablation.csv", "r") as f:
        reader = csv.reader(f)
        next(reader)
        for line in reader:
            (
                _,
                samples_size,
                method,
                dt_size,
                fidelity_macro,
                accuracy_macro,
                fidelity_weighted,
                accuracy_weighted,
            ) = line
            samples_size = f"{float(samples_size):.2f}"

            if method not in comparison["dt_size"]:
                comparison["dt_size"][method] = {}
            if samples_size not in comparison["dt_size"][method]:
                comparison["dt_size"][method][samples_size] = []

            if method not in comparison["fidelity_macro"]:
                comparison["fidelity_macro"][method] = {}
            if samples_size not in comparison["fidelity_macro"][method]:
                comparison["fidelity_macro"][method][samples_size] = []

            if method not in comparison["fidelity_weighted"]:
                comparison["fidelity_weighted"][method] = {}
            if samples_size not in comparison["fidelity_weighted"][method]:
                comparison["fidelity_weighted"][method][samples_size] = []

            if method not in comparison["accuracy_macro"]:
                comparison["accuracy_macro"][method] = {}
            if samples_size not in comparison["accuracy_macro"][method]:
                comparison["accuracy_macro"][method][samples_size] = []

            if method not in comparison["accuracy_weighted"]:
                comparison["accuracy_weighted"][method] = {}
            if samples_size not in comparison["accuracy_weighted"][method]:
                comparison["accuracy_weighted"][method][samples_size] = []

            comparison["dt_size"][method][samples_size].append(int(dt_size))
            comparison["fidelity_macro"][method][samples_size].append(float(fidelity_macro))
            comparison["accuracy_macro"][method][samples_size].append(float(accuracy_macro))
            comparison["fidelity_weighted"][method][samples_size].append(float(fidelity_weighted))
            comparison["accuracy_weighted"][method][samples_size].append(float(accuracy_weighted))

    plots_dir = f"{OUTPUT_PATH}/ablation/plots"
    if not os.path.exists(plots_dir):
        os.makedirs(plots_dir)

    for (metric, methods) in comparison.items():
        samples_sizes = list(methods.values())[0]
        x = list(samples_sizes.keys())

        labels = [method_name for (method_name, samples_sizes) in methods.items()]
        y = [
            [mean_confidence_interval(samples) for samples in samples_sizes.values()]
            for (method_name, samples_sizes) in methods.items()
        ]

        plt.figure(figsize=(30, 3))  # width:20, height:3
        width = 0.3
        fig, ax = plt.subplots()
        locs = np.arange(len(x))  # the label locations
        num_col = len(x) - 1
        width = 0.95 / num_col
        colors = [
            "#d75d5b",
            "#a7c3cd",
            "#524a47",
            "#8a4444",
            "#c8c5c3",
            "#524a47",
            "#edeef0",
        ]

        for idx, values in enumerate(y):
            means = [val[0] for val in values]
            yerr = [val[2] - val[1] for val in values]
            delta_p = 0.125 + (width * idx)
            ax.bar(
                [p + delta_p for p in locs],
                means,
                width,
                yerr=yerr,
                label=labels[idx],
            )

        ax.set_xticks(locs)
        ax.set_xticklabels(x, rotation=60)
        plt.title(f"{metric}")
        plt.legend()
        fig.tight_layout()
        plt.savefig(f"{plots_dir}/plot_{metric}.pdf")
        plt.close()


if __name__ == "__main__":
    # main()
    plot_results()
