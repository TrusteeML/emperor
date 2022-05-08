import os
import numpy as np
import pandas as pd

from sklearn.metrics import classification_report

import input_data
from deeptraffic import DeepTraffic
from trepan.trepan import Trepan, Oracle

DATA_DIR = (
    "../../../../use_cases/vpn_case/res/dataset/train_test/2class/SessionAllLayers"
)
MODEL_DIR = os.path.split(DATA_DIR)[1]

CLASS_NUM = 2
dict_2class = {0: "Novpn", 1: "Vpn"}


dataset = input_data.read_data_sets(DATA_DIR, one_hot=True, num_classes=CLASS_NUM)
class_names = dict_2class.values()
print("Initializing DeepTraffic")
deep_traffic = DeepTraffic()
deep_traffic.fit(dataset.train, model_dir=MODEL_DIR)

X_train = pd.DataFrame(dataset.train.images)
y_train = pd.DataFrame(np.array([np.argmax(i) for i in dataset.train.labels]))
X_test = pd.DataFrame(dataset.test.images)
y_test = pd.DataFrame(np.array([np.argmax(i) for i in dataset.test.labels]))

print("Testing DeepTraffic")
y_pred = deep_traffic.predict(X_test)
print(classification_report(y_test, y_pred, digits=3, target_names=class_names))


oracle = Oracle(deep_traffic, CLASS_NUM, X_train)

# build tree with TREPAN
MIN_EXAMPLES_PER_NODE = 30
MAX_NODES = 200
root = Trepan.build_tree(MIN_EXAMPLES_PER_NODE, MAX_NODES, X_train, oracle)

# calculate fidelity
num_test_examples = X_test.shape[0]
correct = 0
for i in range(0, num_test_examples):
    ann_prediction = oracle.get_oracle_label(X_test.iloc[i, :])
    tree_prediction = root.classify(X_test.iloc[i, :])
    correct += ann_prediction == tree_prediction

fidelity = float(correct) / num_test_examples

print("Fidelity of the model is : " + str(fidelity))

Trepan.plot(root, "./trepan")
