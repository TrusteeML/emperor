import pprint

import shap

import numpy as np
import cv2
import torch
import matplotlib.pyplot as plt
import torch.utils.data as utils
import torch.nn as nn
import torch.nn.functional as F
from torch.autograd import Variable

from skexplain.utils import log

from matplotlib import rcParams
from matplotlib.colors import LinearSegmentedColormap

FONT_NAME = "Roboto"
FONT_WEIGHT = "light"

rcParams["font.family"] = "serif"
rcParams["font.serif"] = [FONT_NAME]
rcParams["font.weight"] = FONT_WEIGHT

# from torchvision.utils import make_grid as make_grid


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
# translation_matrix = np.float32([[1, 0, 0], [0, 1, 0]])
# img_translation = cv2.warpAffine(cow, translation_matrix, (num_cols, num_rows))
# plt.imshow(img_translation, cmap="gray")


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

# since shuffle=True, this is a random sample of test data
batch = next(iter(train_loader))
images, _ = batch
print("before", images.size())
images = Variable(images).view(-1, 200 * 200)
print("before", images.size())
e = shap.DeepExplainer(net, images)


batch = next(iter(train_loader))
train_images, _ = batch
train_images = Variable(train_images).view(-1, 200 * 200)
n_train_images = 5
train_images = images[:n_train_images]
shap_values = e.shap_values(train_images)

shap_values = [np.asarray(s).reshape(-1, 200, 200) for s in shap_values]
train_images = train_images.view(-1, 200, 200)

shap_numpy = [np.swapaxes(np.swapaxes(s, 1, -1), 1, 2) for s in shap_values]
train_numpy = np.swapaxes(np.swapaxes(train_images.numpy(), 1, -1), 1, 2)


pprint.pprint(np.asarray(shap_numpy).shape)
pprint.pprint(train_numpy.shape)


colors = []
for i in np.linspace(1, 0, 100):
    colors.append((215 / 255, 93 / 255, 91 / 255, i))

for i in np.linspace(0, 1, 100):
    colors.append((167 / 255, 195 / 255, 205 / 255, i))

cm = LinearSegmentedColormap.from_list("shap", colors)
class_names = ["Star", "Moon"]
# plot our explanations
fig, axes = plt.subplots(nrows=n_train_images, ncols=len(shap_values) + 1, figsize=(12, 4))
for idx, img in enumerate(train_numpy):
    axes[idx][0].imshow(img)
    axes[idx][0].axis("off")
    max_val = np.max([np.max(np.abs(shap_values[i][:, :-1])) for i in range(len(shap_values))])
    for i in range(len(shap_values)):
        if idx == 0:
            axes[idx][i + 1].set_title(class_names[i])
        axes[idx][i + 1].imshow(img, alpha=0.15)
        im = axes[idx][i + 1].imshow(shap_values[i][idx], cmap=cm, vmin=-max_val, vmax=max_val)
        axes[idx][i + 1].axis("off")

cb = fig.colorbar(
    im,
    ax=axes.ravel().tolist(),
    label="SHAP value",
    orientation="horizontal",
    aspect=60,
)
cb.outline.set_visible(False)
plt.savefig("res/output/shap_values_train.pdf")
plt.show()


# since shuffle=True, this is a random sample of test data
batch = next(iter(test_loader))
images, _ = batch
print("before", images.size())
images = Variable(images).view(-1, 200 * 200)
print("before", images.size())
e = shap.DeepExplainer(net, images)


batch = next(iter(test_loader))
test_images, _ = batch
test_images = Variable(test_images).view(-1, 200 * 200)
n_test_images = 5
test_images = images[:n_test_images]
shap_values = e.shap_values(test_images)

shap_values = [np.asarray(s).reshape(-1, 200, 200) for s in shap_values]
test_images = test_images.view(-1, 200, 200)

shap_numpy = [np.swapaxes(np.swapaxes(s, 1, -1), 1, 2) for s in shap_values]
test_numpy = np.swapaxes(np.swapaxes(test_images.numpy(), 1, -1), 1, 2)


pprint.pprint(np.asarray(shap_numpy).shape)
pprint.pprint(test_numpy.shape)


colors = []
for i in np.linspace(1, 0, 100):
    colors.append((215 / 255, 93 / 255, 91 / 255, i))

for i in np.linspace(0, 1, 100):
    colors.append((167 / 255, 195 / 255, 205 / 255, i))

cm = LinearSegmentedColormap.from_list("shap", colors)
class_names = ["Star", "Moon"]
# plot our explanations
fig, axes = plt.subplots(nrows=n_test_images, ncols=len(shap_values) + 1, figsize=(12, 4))
for idx, img in enumerate(test_numpy):
    axes[idx][0].imshow(img)
    axes[idx][0].axis("off")
    max_val = np.max([np.max(np.abs(shap_values[i][:, :-1])) for i in range(len(shap_values))])
    for i in range(len(shap_values)):
        if idx == 0:
            axes[idx][i + 1].set_title(class_names[i])
        axes[idx][i + 1].imshow(img, alpha=0.15)
        im = axes[idx][i + 1].imshow(shap_values[i][idx], cmap=cm, vmin=-max_val, vmax=max_val)
        axes[idx][i + 1].axis("off")

cb = fig.colorbar(
    im,
    ax=axes.ravel().tolist(),
    label="SHAP value",
    orientation="horizontal",
    aspect=60,
)
cb.outline.set_visible(False)
plt.savefig("res/output/shap_values_test.pdf")
plt.show()

# shap.image_plot(shap_numpy, test_numpy)
