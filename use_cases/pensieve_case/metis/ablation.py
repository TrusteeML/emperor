# Copyright 2018-2019 MIT
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

import os
import csv
import sys
import graphviz
import scipy.stats
import numpy as np
import pandas as pd
from unittest import skip
import matplotlib.pyplot as plt

from dqn import *
from dt import *
from load_trace import *
from log import *
from pensieve_viper_env import *
from rl import *

from sklearn import tree
from sklearn.metrics import f1_score, classification_report

from trustee import ClassificationTrustee
from trustee.report import trust_report
from sklearn.model_selection import train_test_split


from sklearn_porter import Porter


OUTPUT_PATH = "./output"
TRAIN_TRACES = "../cooked_traces/"


def main(leaf_nodes):
    # parameters
    log_fname = "./pensieve_dt.log"
    model_path = "./models/pretrain_linear_reward.ckpt"
    n_batch_rollouts = 10
    max_samples = 200000
    max_iters = 100
    train_frac = 0.8
    is_reweight = False
    n_test_rollouts = 50
    save_dirname = "./decision_tree"
    save_fname = "pensieve_dt_policy_" + leaf_nodes + ".pk"
    save_viz_fname = "pensieve_dt_policy_" + leaf_nodes + ".svg"
    is_train = False
    class_names = ["300", "750", "1200", "1850", "2850", "4300"]

    parameters = {}
    parameters["MILLISECONDS_IN_SECOND"] = 1000.0
    parameters["B_IN_MB"] = 1000000.0
    parameters["BITS_IN_BYTE"] = 8.0
    parameters["RANDOM_SEED"] = 42
    parameters["VIDEO_CHUNCK_LEN"] = 4000.0  # millisec, every time add this amount to buffer
    parameters["BITRATE_LEVELS"] = 6
    parameters["TOTAL_VIDEO_CHUNCK"] = 48
    parameters["BUFFER_THRESH"] = 60.0 * parameters["MILLISECONDS_IN_SECOND"]  # millisec, max buffer limit
    parameters["DRAIN_BUFFER_SLEEP_TIME"] = 500.0  # millisec
    parameters["PACKET_PAYLOAD_PORTION"] = 0.95
    parameters["LINK_RTT"] = 80  # millisec
    parameters["PACKET_SIZE"] = 1500  # bytes
    parameters["NOISE_LOW"] = 0.9
    parameters["NOISE_HIGH"] = 1.1
    parameters["VIDEO_SIZE_FILE"] = "./video/video_size_"
    # bit_rate, buffer_size, next_chunk_size, bandwidth_measurement(throughput and time), chunk_til_video_end
    parameters["S_INFO"] = 6
    parameters["S_LEN"] = 8  # take how many frames in the past
    parameters["A_DIM"] = 6
    parameters["ACTOR_LR_RATE"] = 0.0001
    parameters["CRITIC_LR_RATE"] = 0.001
    parameters["VIDEO_BIT_RATE"] = [300, 750, 1200, 1850, 2850, 4300]  # Kbps
    parameters["BUFFER_NORM_FACTOR"] = 10.0
    parameters["CHUNK_TIL_VIDEO_END_CAP"] = 48.0
    parameters["M_IN_K"] = 1000.0
    parameters["REBUF_PENALTY"] = 4.3  # 1 sec rebuffering -> 3 Mbps
    parameters["SMOOTH_PENALTY"] = 1
    parameters["DEFAULT_QUALITY"] = 1  # default video quality without agent
    parameters["RANDOM_SEED"] = 42
    parameters["RAND_RANGE"] = 1000
    parameters["SUMMARY_DIR"] = "./results"
    parameters["LOG_FILE"] = "./results/log_sim_rl"

    feature_names = ["last_qoe", "last_buffer"]
    for i in range(parameters["S_LEN"]):
        feature_names.append("throughput_" + str(i))
    for i in range(parameters["S_LEN"]):
        feature_names.append("download_" + str(i))
    for i in range(parameters["A_DIM"]):
        feature_names.append("next_size_" + str(i))
    feature_names.append("remain")

    all_cooked_time, all_cooked_bw, all_file_names = load_trace(TRAIN_TRACES)
    parameters["ALL_FILE_NAMES"] = all_file_names

    # Logging
    set_file(log_fname)

    # Data structures
    env = Environment(
        all_cooked_time=all_cooked_time,
        all_cooked_bw=all_cooked_bw,
        parameters=parameters,
    )
    teacher = DQNPolicy(env, model_path, parameters, n_batch_rollouts)

    max_leaf_nodes = None
    if leaf_nodes != "None":
        max_leaf_nodes = int(leaf_nodes)
    max_depth = None
    student = DTPolicy(max_depth, max_leaf_nodes, parameters)

    # Train student
    if is_train:
        student = train_dagger(
            env,
            teacher,
            student,
            max_iters,
            n_batch_rollouts,
            max_samples,
            train_frac,
            is_reweight,
            n_test_rollouts,
            parameters,
            feature_names,
        )
        save_dt_policy(student, save_dirname, save_fname)
        save_dt_policy_viz(student, save_dirname, save_viz_fname, feature_names=feature_names)
    else:
        student = load_dt_policy(save_dirname, save_fname)

    # Test student
    rew = test_policy(env, student, n_test_rollouts, parameters)
    log("Final reward: {}".format(rew), INFO)
    log("Number of nodes: {}".format(student.tree.tree_.node_count), INFO)

    log("FIDELITY TEST START", INFO)
    rollouts = get_rollouts(env, teacher, 1000, parameters, is_student=False)

    # teacher_obss = [state for state, _, _, _, _ in rollouts]
    X = np.array([serilized_state for _, _, _, serilized_state, _ in rollouts])
    y = np.array(teacher.predict_serialized(X))
    student_y = student.predict(X)
    log(classification_report(y, student_y), INFO)
    log("FIDELITY TEST END", INFO)

    porter = Porter(student.tree, language="js")
    output = porter.export(embed_data=True)
    with open(f"{OUTPUT_PATH}/metisDt.js", "w") as writer:
        writer.write(output)

    X_indexes = np.arange(0, X.shape[0])
    X_train, X_test, y_train, y_test = train_test_split(X_indexes, y, train_size=0.7)
    X_train = X[X_train]
    X_test = X[X_test]
    y_pred = np.array(teacher.predict_serialized(X_test))

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

                size = int(int(len(X_train)) * samples_size)
                samples_idxs = np.random.choice(len(X_train), size=size, replace=False)
                X_iter, y_iter = X_train[samples_idxs], y_train[samples_idxs]

                X_sample_train, _, _, _ = train_test_split(X_iter, y_iter, train_size=train_size)
                y_pred_train = teacher.predict_serialized(X_sample_train)

                dt = tree.DecisionTreeClassifier()
                dt = dt.fit(X_sample_train, y_pred_train)
                dt_y_pred = dt.predict(X_test)

                log("Straw-man explanation global fidelity report:", INFO)
                log("\n{}".format(classification_report(y_pred, dt_y_pred, digits=3)), INFO)

                log("Straw-man explanation classification report:", INFO)
                log("\n{}".format(classification_report(y_test, dt_y_pred, digits=3)), INFO)

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
                ######### NODAGGER + ACCURACY #########
                #######################################

                log("Using Classification Trustee algorithm to extract DT...", INFO)
                dagger = ClassificationTrustee(expert=teacher)

                dagger.fit(
                    X_train,
                    y_train,
                    num_iter=num_iter,
                    train_size=train_size,
                    samples_size=samples_size,
                    predict_method_name="predict_serialized",
                    optimization="accuracy",
                    aggregate=False,
                    verbose=True,
                )

                log("###################### Explanation validation ######################", INFO)
                (dt, reward, idx) = dagger.explain()

                log("Accuracy-based  model explanation {} local fidelity: {}".format(idx, reward), INFO)
                dt_y_pred = dt.predict(X_test)

                log("Accuracy-based model explanation w/o dataset aggregation global fidelity report:", INFO)
                log("\n{}".format(classification_report(y_pred, dt_y_pred, digits=3)), INFO)

                log("Accuracy-based model explanation w/o dataset aggregation classification report:", INFO)
                log("\n{}".format(classification_report(y_test, dt_y_pred, digits=3)), INFO)

                writer.writerow(
                    [
                        i,
                        samples_size,
                        "no_dagger_accuracy",
                        dt.tree_.node_count,
                        f1_score(y_pred, dt_y_pred, average="macro"),
                        f1_score(y_test, dt_y_pred, average="macro"),
                        f1_score(y_pred, dt_y_pred, average="weighted"),
                        f1_score(y_test, dt_y_pred, average="weighted"),
                    ]
                )

                #######################################
                ######### NODAGGER + FIDELITY #########
                #######################################

                log("Using Classification Trustee algorithm to extract DT...", INFO)
                dagger = ClassificationTrustee(expert=teacher)

                dagger.fit(
                    X_train,
                    y_train,
                    num_iter=num_iter,
                    train_size=train_size,
                    samples_size=samples_size,
                    predict_method_name="predict_serialized",
                    optimization="accuracy",
                    aggregate=False,
                    verbose=True,
                )

                log("###################### Explanation validation ######################", INFO)
                (dt, reward, idx) = dagger.explain()

                log("Accuracy-based  model explanation {} local fidelity: {}".format(idx, reward), INFO)
                dt_y_pred = dt.predict(X_test)

                log("Accuracy-based model explanation w/o dataset aggregation global fidelity report:", INFO)
                log("\n{}".format(classification_report(y_pred, dt_y_pred, digits=3)), INFO)

                log("Accuracy-based model explanation w/o dataset aggregation classification report:", INFO)
                log("\n{}".format(classification_report(y_test, dt_y_pred, digits=3)), INFO)

                writer.writerow(
                    [
                        i,
                        samples_size,
                        "no_dagger_fidelity",
                        dt.tree_.node_count,
                        f1_score(y_pred, dt_y_pred, average="macro"),
                        f1_score(y_test, dt_y_pred, average="macro"),
                        f1_score(y_pred, dt_y_pred, average="weighted"),
                        f1_score(y_test, dt_y_pred, average="weighted"),
                    ]
                )

                #####################################
                ######### DAGGER + ACCURACY #########
                #####################################

                log("Using Classification Trustee algorithm to extract DT...", INFO)
                dagger = ClassificationTrustee(expert=teacher)

                dagger.fit(
                    X_train,
                    y_train,
                    num_iter=num_iter,
                    predict_method_name="predict_serialized",
                    train_size=train_size,
                    samples_size=samples_size,
                    optimization="accuracy",
                    verbose=True,
                )

                log("###################### Explanation validation ######################", INFO)
                (dt, reward, idx) = dagger.explain()

                log("Accuracy-based  model explanation {} local fidelity: {}".format(idx, reward), INFO)
                dt_y_pred = dt.predict(X_test)

                log("Accuracy-based model explanation global fidelity report:", INFO)
                log("\n{}".format(classification_report(y_pred, dt_y_pred, digits=3)), INFO)

                log("Accuracy-based  model explanation classification report:", INFO)
                log("\n{}".format(classification_report(y_test, dt_y_pred, digits=3)), INFO)

                writer.writerow(
                    [
                        i,
                        samples_size,
                        "dagger_accuracy",
                        dt.tree_.node_count,
                        f1_score(y_pred, dt_y_pred, average="macro"),
                        f1_score(y_test, dt_y_pred, average="macro"),
                        f1_score(y_pred, dt_y_pred, average="weighted"),
                        f1_score(y_test, dt_y_pred, average="weighted"),
                    ]
                )

                #####################################
                ######### DAGGER + FIDELITY #########
                #####################################

                log("Using Classification Trustee algorithm to extract DT...", INFO)
                dagger = ClassificationTrustee(expert=teacher)

                dagger.fit(
                    X_train,
                    y_train,
                    predict_method_name="predict_serialized",
                    num_iter=num_iter,
                    train_size=train_size,
                    samples_size=samples_size,
                    verbose=True,
                )

                log("###################### Explanation validation ######################", INFO)
                (dt, reward, idx) = dagger.explain()

                log("Fidelity-based model explanation {} local fidelity: {}".format(idx, reward), INFO)
                dt_y_pred = dt.predict(X_test)

                log("Fidelity-based Model explanation global fidelity report:", INFO)
                log("\n{}".format(classification_report(y_pred, dt_y_pred, digits=3)), INFO)

                log("Fidelity-based model explanation classification report:", INFO)
                log("\n{}".format(classification_report(y_test, dt_y_pred, digits=3)), INFO)

                writer.writerow(
                    [
                        i,
                        samples_size,
                        "dagger_fidelity",
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
        width = 0.1
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
    # main("100")
    plot_results()
