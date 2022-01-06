import random
import graphviz

from matplotlib import image
import numpy as np
import cv2
import torch
import matplotlib.pyplot as plt
import torch.utils.data as utils
import torch.nn as nn
import torch.nn.functional as F
from torch.autograd import Variable

from pprint import pprint

from sklearn import tree
from sklearn.metrics import classification_report
from skexplain.utils import log
from skexplain.imitation import ClassificationDagger
from skexplain.report import trust_report

from torchvision.utils import make_grid as make_grid


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

    def fit(self, X, y, batch_size=100, epochs=5):
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
                            epoch + 1, batch_idx * len(data), len(train_loader.dataset), bs * batch_idx / len(train_loader), loss.item()
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
# net.fit(biased_data, labels)

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

# logger.log("Testing Neural Network")
# y_pred = net.predict(X_train)
# logger.log("{}".format(classification_report(y_test, y_pred, digits=3)))

# logger.log("Using Classification Dagger algorithm to extract DT...")
# dagger = ClassificationDagger(expert=net)
# dagger.fit(
#     X_train,
#     y_test,
#     num_iter=100,
#     max_leaf_nodes=None,
#     # num_samples=10,
#     samples_size=0.5,
#     # ccp_alpha=0.00000001,
#     verbose=True,
# )

# logger.log("#" * 10, "Explanation validation", "#" * 10)
# (dt, reward, idx) = dagger.explain()

# logger.log("Model explanation {} training fidelity: {}".format(idx, reward))
# dt_y_pred = dt.predict(X_train)

# logger.log("Model explanation test fidelity report:")
# logger.log(
#     "\n{}".format(
#         classification_report(
#             y_pred,
#             dt_y_pred,
#             digits=3,
#         )
#     )
# )

# logger.log("Model explanation classification report:")
# logger.log(
#     "\n{}".format(
#         classification_report(
#             y_test,
#             dt_y_pred,
#             digits=3,
#         )
#     )
# )

# dot_data = tree.export_graphviz(
#     dt,
#     class_names=["star", "moon"],  # sorted(y.unique()),  # [1:] to remove Kali linux instance
#     # feature_names=X.columns,
#     filled=True,
#     rounded=True,
#     special_characters=True,
# )
# graph = graphviz.Source(dot_data)
# graph.render("res/output/dt_{}_{}_{}".format("PyTorchNet", "dagger", dt.get_n_leaves()))

# students = dagger.get_students()
# for (dt, reward, idx) in students:
#     if reward >= 0.99:
#         dot_data = tree.export_graphviz(
#             dt,
#             class_names=["star", "moon"],  # sorted(y.unique()),  # [1:] to remove Kali linux instance
#             # feature_names=X.columns,
#             filled=True,
#             rounded=True,
#             special_characters=True,
#         )
#         graph = graphviz.Source(dot_data)
#         graph.render("res/output/trees/dt_{}_{}_{}_{}_{}".format("PyTorchNet", "dagger", dt.get_n_leaves(), reward, idx))

trust_report(
    net,
    X_train=X_train,
    X_test=X_test,
    y_train=y_train,
    y_test=y_test,
    class_names=["star", "moon"],
    output="res/output/dt_trust_report.pdf",
    logger=logger,
    verbose=True,
)
