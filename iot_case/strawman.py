import os
import csv
import graphviz
import scipy.stats
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt

from skexplain.imitation import ClassificationTrustee
from skexplain.utils import dataset, log
from skexplain.utils.const import IOT_DATASET_META

from sklearn import tree
from sklearn.metrics import f1_score, classification_report
from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestClassifier


OUTPUT_PATH = "res/output"
DF_DATASET_PATH = "res/dataset/zip_files/16-09-23-labeled.csv.zip"
IOT_DATASET_META["is_dir"] = False

COLORS = [
    "#d75d5b",
    "#a7c3cd",
    "#524a47",
    "#8a4444",
    "#c8c5c3",
    "#524a47",
    "#edeef0",
]


def mean_confidence_interval(data, confidence=0.95):
    a = 1.0 * np.array(data)
    n = len(a)
    m, se = np.mean(a), scipy.stats.sem(a)
    h = se * scipy.stats.t.ppf((1 + confidence) / 2.0, n - 1)
    return m, m - h, m + h


def plot_results_no_contraints():
    """Plots results of strawman approach comparison"""
    comparison = {
        "dt_size": {},
        "fidelity_macro": {},
        "accuracy_macro": {},
        "fidelity_weighted": {},
        "accuracy_weighted": {},
    }

    output_dir = f"{OUTPUT_PATH}/strawman"
    with open(f"{output_dir}/strawman_no_contraints.csv", "r") as f:
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

    plots_dir = f"{OUTPUT_PATH}/strawman/plots_no_contraints"
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
        fig, ax = plt.subplots()
        locs = np.arange(len(x))  # the label locations
        num_col = len(x) - 1
        width = 0.95 / num_col

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


def plot_results_max_leaves():
    """Plots results of strawman approach comparison"""
    comparison = {
        "dt_num_leaves": {},
        "fidelity_macro": {},
        "accuracy_macro": {},
        "fidelity_weighted": {},
        "accuracy_weighted": {},
    }

    output_dir = f"{OUTPUT_PATH}/strawman"
    with open(f"{output_dir}/strawman_max_leaves.csv", "r") as f:
        reader = csv.reader(f)
        next(reader)
        for line in reader:
            (
                _,
                max_leaves,
                method,
                _,
                _,
                _,
                dt_num_leaves,
                fidelity_macro,
                accuracy_macro,
                fidelity_weighted,
                accuracy_weighted,
            ) = line

            if method not in comparison["dt_num_leaves"]:
                comparison["dt_num_leaves"][method] = {}
            if max_leaves not in comparison["dt_num_leaves"][method]:
                comparison["dt_num_leaves"][method][max_leaves] = []

            if method not in comparison["fidelity_macro"]:
                comparison["fidelity_macro"][method] = {}
            if max_leaves not in comparison["fidelity_macro"][method]:
                comparison["fidelity_macro"][method][max_leaves] = []

            if method not in comparison["fidelity_weighted"]:
                comparison["fidelity_weighted"][method] = {}
            if max_leaves not in comparison["fidelity_weighted"][method]:
                comparison["fidelity_weighted"][method][max_leaves] = []

            if method not in comparison["accuracy_macro"]:
                comparison["accuracy_macro"][method] = {}
            if max_leaves not in comparison["accuracy_macro"][method]:
                comparison["accuracy_macro"][method][max_leaves] = []

            if method not in comparison["accuracy_weighted"]:
                comparison["accuracy_weighted"][method] = {}
            if max_leaves not in comparison["accuracy_weighted"][method]:
                comparison["accuracy_weighted"][method][max_leaves] = []

            comparison["dt_num_leaves"][method][max_leaves].append(int(dt_num_leaves))
            comparison["fidelity_macro"][method][max_leaves].append(float(fidelity_macro))
            comparison["accuracy_macro"][method][max_leaves].append(float(accuracy_macro))
            comparison["fidelity_weighted"][method][max_leaves].append(float(fidelity_weighted))
            comparison["accuracy_weighted"][method][max_leaves].append(float(accuracy_weighted))

    plots_dir = f"{OUTPUT_PATH}/strawman/plots_max_leaves"
    if not os.path.exists(plots_dir):
        os.makedirs(plots_dir)

    fidelity = []
    leaves = []
    for (metric, methods) in comparison.items():
        max_leaves_list = list(methods.values())[0]
        x = list(max_leaves_list.keys())

        labels = [method_name for (method_name, max_leaves_list) in methods.items()]
        y = [
            [mean_confidence_interval(samples) for samples in max_leaves_list.values()]
            for (method_name, max_leaves_list) in methods.items()
        ]

        if "dt_num_leaves" == metric:
            leaves = y

        if "fidelity_macro" == metric:
            fidelity = y

        plt.figure(figsize=(30, 3))  # width:20, height:3
        fig, ax = plt.subplots()
        locs = np.arange(len(x))  # the label locations
        num_col = len(x) - 1
        width = 0.95 / num_col

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

    plt.figure(figsize=(30, 3))  # width:20, height:3
    fig, ax = plt.subplots()
    # locs = np.arange(len(fidelity))  # the label locations
    # num_col = len(x) - 1
    # width = 0.95 / num_col

    for idx, (x_values, y_values) in enumerate(zip(leaves, fidelity)):
        mean_leaves = [val[0] for val in x_values]
        mean_fidelity = [val[0] for val in y_values]
        yerr = [val[2] - val[1] for val in y_values]

        plt.plot(
            mean_leaves,
            mean_fidelity,
            # yerr=yerr,
            label=labels[idx] if idx < len(labels) else "",
        )

    # ax.set_xticks(locs)
    # ax.set_xticklabels(x, rotation=60)
    plt.title("Fidelity vs. Number of Leaves")
    plt.legend()
    fig.tight_layout()
    plt.savefig(f"{plots_dir}/plot_fidelity_vs_leaves.pdf")
    plt.close()


def compare_methods_no_contraints(
    blackbox,
    X_train,
    y_train,
    X_test,
    y_test,
    y_pred,
    output_dir,
    logger,
):
    """Compares different strawman approaches to ma-trustee with no constraints"""
    num_iter = 50
    train_size = 0.7
    with open(f"{output_dir}/strawman_no_contraints.csv", "w", encoding="utf-8") as f:
        # create the csv writer
        writer = csv.writer(f)
        writer.writerow(
            [
                "iteration",
                "samples_size",
                "method",
                "dt_size",
                "dt_depth",
                "dt_num_leaves",
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
                        "strawman",
                        dt.tree_.node_count,
                        dt.get_depth(),
                        dt.get_n_leaves(),
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
                    verbose=False,
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
                        dt.get_depth(),
                        dt.get_n_leaves(),
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
                    verbose=False,
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
                        dt.get_depth(),
                        dt.get_n_leaves(),
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
                    verbose=False,
                )

                logger.log("#" * 10, "Explanation validation", "#" * 10)
                (dt, reward, idx) = trustee.explain()

                logger.log("Accuracy-based  model explanation {} local fidelity: {}".format(idx, reward))
                dt_y_pred = dt.predict(X_test)

                logger.log("Accuracy-based model explanation global fidelity report:")
                logger.log("\n{}".format(classification_report(y_pred, dt_y_pred, digits=3)))

                logger.log("Accuracy-based  model explanation classification report:")
                logger.log("\n{}".format(classification_report(y_test, dt_y_pred, digits=3)))

                writer.writerow(
                    [
                        i,
                        samples_size,
                        "trustee_accuracy",
                        dt.tree_.node_count,
                        dt.get_depth(),
                        dt.get_n_leaves(),
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
                    verbose=False,
                )

                logger.log("#" * 10, "Explanation validation", "#" * 10)
                (dt, reward, idx) = trustee.explain()

                logger.log("Fidelity-based model explanation {} local fidelity: {}".format(idx, reward))
                dt_y_pred = dt.predict(X_test)

                logger.log("Fidelity-based Model explanation global fidelity report:")
                logger.log("\n{}".format(classification_report(y_pred, dt_y_pred, digits=3)))

                logger.log("Fidelity-based model explanation classification report:")
                logger.log("\n{}".format(classification_report(y_test, dt_y_pred, digits=3)))

                writer.writerow(
                    [
                        i,
                        samples_size,
                        "trustee_fidelity",
                        dt.tree_.node_count,
                        dt.get_depth(),
                        dt.get_n_leaves(),
                        f1_score(y_pred, dt_y_pred, average="macro"),
                        f1_score(y_test, dt_y_pred, average="macro"),
                        f1_score(y_pred, dt_y_pred, average="weighted"),
                        f1_score(y_test, dt_y_pred, average="weighted"),
                    ]
                )


def compare_methods_max_leaves(
    blackbox,
    X_train,
    y_train,
    X_test,
    y_test,
    y_pred,
    output_dir,
    logger,
):
    """Compares different strawman approaches to ma-trustee with no constraints"""
    max_dt = tree.DecisionTreeClassifier()
    max_dt = max_dt.fit(X_train, y_train)

    num_iter = 50
    train_size = 0.7
    samples_size = 0.3
    num_quantiles = 10
    with open(f"{output_dir}/strawman_max_leaves.csv", "w", encoding="utf-8") as csv_file:
        # create the csv writer
        writer = csv.writer(csv_file)
        writer.writerow(
            [
                "iteration",
                "max_leaves",
                "method",
                "samples_size",
                "dt_size",
                "dt_depth",
                "dt_num_leaves",
                "fidelity_macro",
                "accuracy_macro",
                "fidelity_weighted",
                "accuracy_weighted",
            ]
        )

        for quantil in np.linspace(0, 1, num_quantiles, endpoint=False):
            max_leaves = int(np.quantile(np.arange(2, max_dt.get_n_leaves()), quantil))
            if max_leaves > 1:
                for i in range(30):
                    #####################################
                    ############# STRAWMAN ##############
                    #####################################

                    size = int(int(len(X_train)) * samples_size)
                    samples_idxs = np.random.choice(len(X_train), size=size, replace=False)
                    X_iter, y_iter = X_train.iloc[samples_idxs], y_train.iloc[samples_idxs]

                    X_sample_train, _, _, _ = train_test_split(X_iter, y_iter, train_size=train_size)
                    y_pred_train = blackbox.predict(X_sample_train)

                    dt = tree.DecisionTreeClassifier(max_leaf_nodes=max_leaves)
                    dt = dt.fit(X_sample_train, y_pred_train)
                    dt_y_pred = dt.predict(X_test)

                    logger.log("Straw-man explanation global fidelity report:")
                    logger.log("\n{}".format(classification_report(y_pred, dt_y_pred, digits=3)))

                    logger.log("Straw-man explanation classification report:")
                    logger.log("\n{}".format(classification_report(y_test, dt_y_pred, digits=3)))

                    writer.writerow(
                        [
                            i,
                            max_leaves,
                            "strawman",
                            samples_size,
                            dt.tree_.node_count,
                            dt.get_depth(),
                            dt.get_n_leaves(),
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
                        max_leaf_nodes=max_leaves,
                        optimization="accuracy",
                        aggregate=False,
                        verbose=False,
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
                            max_leaves,
                            "no_trustee_accuracy",
                            samples_size,
                            dt.tree_.node_count,
                            dt.get_depth(),
                            dt.get_n_leaves(),
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
                        max_leaf_nodes=max_leaves,
                        optimization="accuracy",
                        aggregate=False,
                        verbose=False,
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
                            max_leaves,
                            "no_trustee_fidelity",
                            samples_size,
                            dt.tree_.node_count,
                            dt.get_depth(),
                            dt.get_n_leaves(),
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
                        max_leaf_nodes=max_leaves,
                        optimization="accuracy",
                        verbose=False,
                    )

                    logger.log("#" * 10, "Explanation validation", "#" * 10)
                    (dt, reward, idx) = trustee.explain()

                    logger.log("Accuracy-based  model explanation {} local fidelity: {}".format(idx, reward))
                    dt_y_pred = dt.predict(X_test)

                    logger.log("Accuracy-based model explanation global fidelity report:")
                    logger.log("\n{}".format(classification_report(y_pred, dt_y_pred, digits=3)))

                    logger.log("Accuracy-based  model explanation classification report:")
                    logger.log("\n{}".format(classification_report(y_test, dt_y_pred, digits=3)))

                    writer.writerow(
                        [
                            i,
                            max_leaves,
                            "trustee_accuracy",
                            samples_size,
                            dt.tree_.node_count,
                            dt.get_depth(),
                            dt.get_n_leaves(),
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
                        max_leaf_nodes=max_leaves,
                        verbose=False,
                    )

                    logger.log("#" * 10, "Explanation validation", "#" * 10)
                    (dt, reward, idx) = trustee.explain()

                    logger.log("Fidelity-based model explanation {} local fidelity: {}".format(idx, reward))
                    dt_y_pred = dt.predict(X_test)

                    logger.log("Fidelity-based Model explanation global fidelity report:")
                    logger.log("\n{}".format(classification_report(y_pred, dt_y_pred, digits=3)))

                    logger.log("Fidelity-based model explanation classification report:")
                    logger.log("\n{}".format(classification_report(y_test, dt_y_pred, digits=3)))

                    writer.writerow(
                        [
                            i,
                            max_leaves,
                            "trustee_fidelity",
                            samples_size,
                            dt.tree_.node_count,
                            dt.get_depth(),
                            dt.get_n_leaves(),
                            f1_score(y_pred, dt_y_pred, average="macro"),
                            f1_score(y_test, dt_y_pred, average="macro"),
                            f1_score(y_pred, dt_y_pred, average="weighted"),
                            f1_score(y_test, dt_y_pred, average="weighted"),
                        ]
                    )


def main():
    """Test using Reinforcement Learning to extract Decision Tree from a generic Blackbox model"""
    logger = log.Logger("{}/strawman.log".format(OUTPUT_PATH))

    # Step 1: Load training dataset
    logger.log("#" * 10, "Dataset init", "#" * 10)
    logger.log("Reading dataset from CSV...")
    X, y, feature_names, _, _ = dataset.read(
        DF_DATASET_PATH,
        metadata=IOT_DATASET_META,
        verbose=False,
        logger=logger,
        as_df=True,
    )

    X_indexes = np.arange(0, X.shape[0])
    X_train, X_test, y_train, y_test = train_test_split(X_indexes, y, train_size=0.7)
    X_train = X.iloc[X_train]
    X_test = X.iloc[X_test]
    logger.log("X size: {}; y size: {}".format(len(X), len(y)))
    logger.log("Done!")

    logger.log("Initializing model: {}...".format("RandomForestClassifier"))
    blackbox = RandomForestClassifier(n_jobs=4)
    blackbox.fit(X_train, y_train if isinstance(y_train, pd.DataFrame) else y_train.ravel())
    y_pred = blackbox.predict(X_test)
    logger.log("Done!")

    logger.log("Blackbox model classification report with IID:")
    logger.log("\n{}".format(classification_report(y_test, y_pred, digits=3)))

    output_dir = f"{OUTPUT_PATH}/strawman"
    if not os.path.exists(output_dir):
        os.makedirs(output_dir)

    # compare_methods_no_contraints(
    #     blackbox,
    #     X_train,
    #     y_train,
    #     X_test,
    #     y_test,
    #     y_pred,
    #     output_dir,
    #     logger,
    # )

    compare_methods_max_leaves(
        blackbox,
        X_train,
        y_train,
        X_test,
        y_test,
        y_pred,
        output_dir,
        logger,
    )


if __name__ == "__main__":
    # main()
    # plot_results_no_contraints()
    plot_results_max_leaves()
