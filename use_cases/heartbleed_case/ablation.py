import os
import csv

import scipy.stats
import numpy as np
import matplotlib.pyplot as plt

from trustee import ClassificationTrustee
from trustee.utils import dataset, log, persist
from trustee.utils.const import CIC_IDS_2017_DATASET_META

from sklearn import tree
from sklearn.metrics import classification_report, f1_score
from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestClassifier

DF_TRAIN_TEST_PATH = "res/dataset/CIC-IDS-2017/"
DF_TRAIN_TEST_OVER_PATH = "res/dataset/CIC-IDS-2017_OverSampled_min.csv.zip"
OUTPUT_PATH = "res/output"

# if using oversampled df
# CIC_IDS_2017_DATASET_META["is_dir"] = False


def main():
    """Test using Reinforcement Learning to extract Decision Tree from a generic Blackbox model"""
    logger = log.Logger("{}/output.log".format(OUTPUT_PATH))

    logger.log("Reading CIC-IDS-2017 dataset...")
    # Step 1: Parse train-test def
    X, y, _, _, _ = dataset.read(DF_TRAIN_TEST_PATH, metadata=CIC_IDS_2017_DATASET_META, as_df=True)
    logger.log("Done!")

    logger.log("Splitting dataset into training and test...")
    X_indexes = np.arange(0, X.shape[0])
    X_train, X_test, y_train, y_test = train_test_split(X_indexes, y, train_size=0.7, stratify=y)
    X_train = X.iloc[X_train]
    X_test = X.iloc[X_test]
    logger.log("Done!")

    # Step 2: Train black-box model with loaded dataset
    logger.log("#" * 10, "Model init", "#" * 10)
    model_path = "RandomForestClassifier_cic_ids_2017.joblib.zip"
    logger.log("Looking for pre-trained model: {}...".format(model_path))
    blackbox = persist.load_model(model_path)
    if not blackbox:
        logger.log("Training model: RandomForestClassifier...")
        blackbox = RandomForestClassifier(n_jobs=4)
        blackbox.fit(X_train, y_train)
        persist.save_model(blackbox, model_path)

    logger.log("Done!")
    y_pred = blackbox.predict(X_test)

    logger.log("Blackbox model classification report with IID:")
    logger.log("\n{}".format(classification_report(y_test, y_pred, digits=3)))

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

        for samples_size in np.arange(0.001, 0.3, 0.05):
            for i in range(30):
                #####################################
                ############# STRAWMAN ##############
                #####################################

                size = int(int(len(X_train)) * samples_size)
                samples_idxs = np.random.choice(len(X_train), size=size, replace=False)
                X_iter, y_iter = X_train.iloc[samples_idxs], y_train.iloc[samples_idxs]

                X_sample_train, _, _, _ = train_test_split(X_iter, y_iter, train_size=train_size)
                y_pred_train = blackbox.predict(X_sample_train)

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
                trustee = ClassificationTrustee(expert=blackbox)

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
                trustee = ClassificationTrustee(expert=blackbox)

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
                trustee = ClassificationTrustee(expert=blackbox)

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
                trustee = ClassificationTrustee(expert=blackbox)

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
