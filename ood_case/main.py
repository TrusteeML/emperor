import graphviz
import numpy as np

from skexplain.imitation import ClassificationDagger
from skexplain.utils import dataset, log, persist
from skexplain.utils.const import CIC_IDS_2017_DATASET_META

from sklearn import tree
from sklearn.ensemble import RandomForestClassifier
from sklearn.metrics import classification_report
from sklearn.model_selection import train_test_split


DF_TRAIN_TEST_PATH = "res/dataset/CIC-IDS-2017/"
DF_TRAIN_TEST_OVER_PATH = "res/dataset/CIC-IDS-2017_OverSampled.csv.zip"
DF_VALIDATE_PATH = "res/dataset/validation/heartbleed.csv"

# if using oversampled df
CIC_IDS_2017_DATASET_META["is_dir"] = False


def main():
    logger = log.Logger("res/output/output.log")

    logger.log("Reading CIC-IDS-2017 dataset...")
    # Step 1: Parse train-test def
    X, y, feature_names, _, _ = dataset.read(DF_TRAIN_TEST_OVER_PATH, metadata=CIC_IDS_2017_DATASET_META, as_df=True)
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
    logger.log(
        "\n{}".format(
            classification_report(
                y_test,
                y_pred,
                digits=3,
                target_names=CIC_IDS_2017_DATASET_META["classes"],
            )
        )
    )

    logger.log("Reading Heartbleed OOD dataset...")
    df_meta = CIC_IDS_2017_DATASET_META
    df_meta["is_dir"] = False
    X_validate, y_validate, _, _, _ = dataset.read(DF_VALIDATE_PATH, metadata=df_meta, as_df=True)
    logger.log("Done!")

    y_val_pred = blackbox.predict(X_validate)

    logger.log("Blackbox model classification report with OOD:")
    logger.log(
        "\n{}".format(
            classification_report(
                y_validate,
                y_val_pred,
                digits=3,
                target_names=["BENIGN", "Heartbleed"],
            )
        )
    ), 0

    # Decision tree extraction
    logger.log("Using Classification Dagger algorithm to extract DT...")
    dagger = ClassificationDagger(expert=blackbox)

    dagger.fit(
        X_train,
        y_train,
        max_iter=100,
        max_leaf_nodes=None,
        num_samples=100000,
        # samples_size=0.01,
        # ccp_alpha=0.00000001,
        verbose=True,
    )

    logger.log("#" * 10, "Explanation validation", "#" * 10)
    (dt, reward, idx) = dagger.explain()

    logger.log("Model explanation {} local fidelity: {}".format(idx, reward))
    dt_y_pred = dt.predict(X_test)

    class_names = CIC_IDS_2017_DATASET_META["classes"]
    logger.log("Model explanation global fidelity report:")
    logger.log(
        "\n{}".format(
            classification_report(
                y_pred,
                dt_y_pred,
                digits=3,
                target_names=class_names,
            )
        )
    )

    logger.log("Model explanation classification report:")
    logger.log(
        "\n{}".format(
            classification_report(
                y_test,
                dt_y_pred,
                digits=3,
                target_names=class_names,
            )
        )
    )

    dot_data = tree.export_graphviz(
        dt,
        class_names=class_names,
        feature_names=feature_names,
        filled=True,
        rounded=True,
        special_characters=True,
    )
    graph = graphviz.Source(dot_data)
    graph.render("res/output/dt_{}_{}_{}".format("RandomForest", "dagger", dt.get_n_leaves()))


if __name__ == "__main__":
    main()
