import os
import sys
import numpy as np

from sklearn.ensemble import RandomForestClassifier
from sklearn.model_selection import train_test_split

from persist import load_model, save_model
from dataset import read
from const import CIC_IDS_2017_DATASET_META

sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from trepan.trepan import Trepan, Oracle

DATA_PATH = "../../../../use_cases/heartbleed_case/res/dataset/CIC-IDS-2017_OverSampled_min.csv.zip"
MODEL_PATH = "../../../../use_cases/heartbleed_case/res/models/RandomForestClassifier_cic_ids_2017.joblib.zip"

# Step 1: Parse train-test def
X, y, feature_names, _, _ = read(
    DATA_PATH, metadata=CIC_IDS_2017_DATASET_META, as_df=True, verbose=True
)
num_classes = np.unique(y)
total_num_examples = X.shape[0]
print("Done!")

print("Splitting dataset into training and test...")
X_indexes = np.arange(0, X.shape[0])
X_train, X_test, y_train, y_test = train_test_split(
    X_indexes, y, train_size=0.7, stratify=y
)
X_train = X.iloc[X_train]
X_test = X.iloc[X_test]
print("Done!")

# Step 2: Train black-box model with loaded dataset
print("#" * 10, "Model init", "#" * 10)
print(f"Looking for pre-trained model: {MODEL_PATH}...")
model = load_model(MODEL_PATH)
if not model:
    print("Training model: RandomForestClassifier...")
    model = RandomForestClassifier(n_jobs=4)
    model.fit(X_train, y_train)
    save_model(model, MODEL_PATH)
print("Done!")

oracle = Oracle(model, num_classes, X_train)

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
