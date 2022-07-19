import os
import csv
import graphviz

import scipy.stats
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt


# from matplotlib import image
import cv2
import torch
import torch.utils.data as utils
import torch.nn as nn
import torch.nn.functional as F
from torch.autograd import Variable

from sklearn import tree
from sklearn.metrics import f1_score, classification_report
from sklearn.model_selection import train_test_split

from skexplain.imitation import ClassificationTrustee
from skexplain.utils import log

# from torchvision.utils import make_grid as make_grid

OUTPUT_PATH = "res/output"


def main():
    """Test using Reinforcement Learning to extract Decision Tree from a generic net model"""
    # Dataset specification
    n = 1000
    dim = 1
    std = 10.0
    # Train specification
    epochs = 100
    lr = 0.0001
    bs = 100
    log_interval = 10

    logger = log.Logger("res/output/output.log")

    bunny = np.load("res/dataset/bunny.npy")
    bunny = bunny

    cow = np.load("res/dataset/cow.npy")
    cow = cow

    num_rows, num_cols = bunny.shape[:2]

    # bottom right: 46 39 to 60 70
    translation_matrix = np.float32([[1, 0, 0], [0, 1, 0]])
    img_translation = cv2.warpAffine(cow, translation_matrix, (num_cols, num_rows))
    plt.imshow(img_translation, cmap="gray")

    biased_train_bun = []
    biased_train_cow = []

    for i in range(1000):
        x_val = np.random.randint(46, 60)
        y_val = np.random.randint(39, 70)
        translation_matrix = np.float32([[1, 0, x_val], [0, 1, y_val]])
        im = cv2.warpAffine(bunny, translation_matrix, (200, 200))
        biased_train_bun.append(im)
        x_val = np.random.randint(-53, -39)
        y_val = np.random.randint(-65, -34)
        translation_matrix = np.float32([[1, 0, x_val], [0, 1, y_val]])
        im = cv2.warpAffine(bunny, translation_matrix, (200, 200))
        biased_train_bun.append(im)

        y_val = np.random.randint(44, 64)
        x_val = np.random.randint(-46, -22)
        translation_matrix = np.float32([[1, 0, x_val], [0, 1, y_val]])
        im = cv2.warpAffine(cow, translation_matrix, (200, 200))
        biased_train_cow.append(im)
        y_val = np.random.randint(-56, -33)
        x_val = np.random.randint(55, 78)
        translation_matrix = np.float32([[1, 0, x_val], [0, 1, y_val]])
        im = cv2.warpAffine(cow, translation_matrix, (200, 200))
        biased_train_cow.append(im)

    unbiased_train_bun = []
    unbiased_train_cow = []

    for i in range(2000):
        x_val = np.random.randint(-53, 60)
        y_val = np.random.randint(-65, 70)
        translation_matrix = np.float32([[1, 0, x_val], [0, 1, y_val]])
        im = cv2.warpAffine(bunny, translation_matrix, (200, 200))
        unbiased_train_bun.append(im)

        y_val = np.random.randint(-56, 64)
        x_val = np.random.randint(-46, 78)
        translation_matrix = np.float32([[1, 0, x_val], [0, 1, y_val]])
        im = cv2.warpAffine(cow, translation_matrix, (200, 200))
        unbiased_train_cow.append(im)

    biased_train_cow = np.array(biased_train_cow)
    biased_train_bun = np.array(biased_train_bun)
    unbiased_train_cow = np.array(unbiased_train_cow)
    unbiased_train_bun = np.array(unbiased_train_bun)

    """# New Section"""

    unbiased_stars = unbiased_train_cow
    unbiased_moons = unbiased_train_bun
    biased_stars = biased_train_cow
    biased_moons = biased_train_bun

    # np.set_printoptions(threshold=sys.maxsize)

    # logger.log("\n".join(["".join(["{}".format(item) for item in row]) for row in biased_stars[0]]))
    # plogger.log(unbiased_stars[0])

    # with open("res/img/map.csv", "w") as f:
    #     count = 0
    #     for row in biased_stars[random.randint(1, 1000)]:
    #         for item in row:
    #             f.write("{},".format(count))
    #             count += 1
    #         f.write("\n")

    # def chunker(seq, size):
    #     return (seq[pos : pos + size] for pos in range(0, len(seq), size))

    # for idx, data in enumerate(chunker(biased_stars, 25)):
    #     grid = make_grid(torch.from_numpy(np.float32(data)).view(25, 1, 200, 200), nrow=5, pad_value=1, padding=10)
    #     plt.axis("off")
    #     plt.imsave("res/img/biased_stars/{}.png".format(idx), grid.numpy().transpose(1, 2, 0))
    #     plt.imshow(grid.numpy().transpose(1, 2, 0))
    #     plt.close()

    # for idx, data in enumerate(chunker(unbiased_stars, 25)):
    #     grid = make_grid(torch.from_numpy(np.float32(data)).view(25, 1, 200, 200), nrow=5, pad_value=1, padding=10)
    #     plt.axis("off")
    #     plt.imsave("res/img/unbiased_stars/{}.png".format(idx), grid.numpy().transpose(1, 2, 0))
    #     plt.imshow(grid.numpy().transpose(1, 2, 0))
    #     plt.close()

    # for idx, data in enumerate(chunker(biased_moons, 25)):
    #     grid = make_grid(torch.from_numpy(np.float32(data)).view(25, 1, 200, 200), nrow=5, pad_value=1, padding=10)
    #     plt.axis("off")
    #     plt.imsave("res/img/biased_moons/{}.png".format(idx), grid.numpy().transpose(1, 2, 0))
    #     plt.imshow(grid.numpy().transpose(1, 2, 0))
    #     plt.close()

    # for idx, data in enumerate(chunker(unbiased_moons, 25)):
    #     grid = make_grid(torch.from_numpy(np.float32(data)).view(25, 1, 200, 200), nrow=5, pad_value=1, padding=10)
    #     plt.axis("off")
    #     plt.imsave("res/img/unbiased_moons/{}.png".format(idx), grid.numpy().transpose(1, 2, 0))
    #     plt.imshow(grid.numpy().transpose(1, 2, 0))
    #     plt.close()

    unbiased_data = np.concatenate((unbiased_stars, unbiased_moons))
    unbiased_data = torch.from_numpy(np.float32(unbiased_data))
    labels = np.concatenate((np.zeros(len(unbiased_stars)), np.ones(len(unbiased_stars))))
    labels = torch.from_numpy(labels).long()
    biased_data = np.concatenate((biased_stars, biased_moons))
    biased_data = torch.from_numpy(np.float32(biased_data))

    train_data = utils.TensorDataset(biased_data, labels)
    train_loader = utils.DataLoader(train_data, batch_size=100, shuffle=True)
    test_data = utils.TensorDataset(unbiased_data, labels)
    test_loader = utils.DataLoader(test_data, batch_size=100)

    # Build FC net
    class Net(nn.Module):
        def __init__(self):
            super(Net, self).__init__()
            self.fc1 = nn.Linear(200 * 200, 1024)
            self.fc2 = nn.Linear(1024, 1024)
            self.fc3 = nn.Linear(1024, 2)

        def forward(self, x):
            x = F.relu(self.fc1(x))
            x = F.relu(self.fc2(x))
            x = self.fc3(x)
            return x

        def fit(self, X, y, batch_size=100, epochs=1):
            train_data = utils.TensorDataset(X, y)
            train_loader = utils.DataLoader(train_data, batch_size=batch_size, shuffle=True)

            lr = 0.001
            optimizer = torch.optim.Adam(net.parameters(), lr=lr)
            # criterion = nn.MSELoss()
            criterion = nn.CrossEntropyLoss()

            for epoch in range(epochs):
                total = 0.0
                correct = 0.0
                for batch_idx, (data, target) in enumerate(train_loader):
                    # data, target = Variable(data).cuda(), Variable(target).cuda()
                    data, target = Variable(data), Variable(target)
                    data = data.view(-1, 200 * 200)
                    target = target.squeeze()
                    optimizer.zero_grad()
                    net_out = net(data).squeeze()
                    loss = criterion(net_out, target)
                    loss.backward()
                    optimizer.step()
                    if batch_idx % log_interval == 0:
                        logger.log(
                            "Train Epoch: {} [{}/{} ({:.0f}%)]\tLoss: {:.6f}".format(
                                epoch + 1,
                                batch_idx * len(data),
                                len(train_loader.dataset),
                                bs * batch_idx / len(train_loader),
                                loss.item(),
                            )
                        )

                    _, predicted = torch.max(net_out.data, 1)
                    total += target.size(0)
                    correct += (predicted == target).sum().item()
                    # logger.log("predicted", "total", predicted, total)
                    # logger.log("target", "correct", target, correct)
            logger.log("Train Acc: " + str(correct / total))

        def predict(self, x):
            net_out = self(x).squeeze()
            _, predicted = torch.max(net_out.data, 1)
            return predicted

    net = Net()
    net.fit(biased_data, labels)

    # total = 0.0
    # correct = 0.0
    # for idx, (data, target) in enumerate(test_loader):
    #     # data, target = Variable(data).cuda(), Variable(target).cuda()
    #     data, target = Variable(data), Variable(target)
    #     data = data.view(-1, 200 * 200)
    #     # optimizer.zero_grad()
    #     net_out = net(data).squeeze()
    #     _, predicted = torch.max(net_out.data, 1)
    #     # logger.log("predicted", predicted)
    #     total += target.size(0)
    #     correct += (predicted == target).sum().item()
    # logger.log("Test Acc: " + str(correct / total))

    X_train = torch.tensor([], dtype=torch.long)
    y_train = torch.tensor([], dtype=torch.long)
    X_test = torch.tensor([], dtype=torch.long)
    y_test = torch.tensor([], dtype=torch.long)

    for idx, (data, target) in enumerate(train_loader):
        X_train = torch.cat((X_train, data.view(-1, 200 * 200)))
        y_train = torch.cat((y_train, target.squeeze()))

    logger.log("X train", X_train.size())
    logger.log("y train", y_train.size())

    for idx, (data, target) in enumerate(test_loader):
        X_test = torch.cat((X_test, data.view(-1, 200 * 200)))
        y_test = torch.cat((y_test, target.squeeze()))

    logger.log("X test", X_test.size())
    logger.log("y test", y_test.size())

    logger.log("Testing Neural Network")
    y_pred = net.predict(X_train)
    logger.log("{}".format(classification_report(y_test, y_pred, digits=3)))

    output_dir = f"{OUTPUT_PATH}/ablation"
    if not os.path.exists(output_dir):
        os.makedirs(output_dir)

    num_iter = 5
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
                X_iter, y_iter = (
                    X_train[samples_idxs].clone().detach(),
                    y_train[samples_idxs].clone().detach(),
                )

                X_sample_train, _, _, _ = train_test_split(X_iter, y_iter, train_size=train_size)
                y_pred_train = net.predict(X_sample_train)

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
                trustee = ClassificationTrustee(expert=net)

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
                trustee = ClassificationTrustee(expert=net)

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
                trustee = ClassificationTrustee(expert=net)

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
                trustee = ClassificationTrustee(expert=net)

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
    # main()
    plot_results()
