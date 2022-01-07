from skexplain.report import trust_report
from skexplain.utils import dataset, log
from skexplain.utils.const import IOT_DATASET_META

from sklearn.tree import DecisionTreeClassifier
from sklearn.ensemble import RandomForestClassifier


OUTPUT_PATH = "res/output"
DF_DATASET_PATH = "res/dataset/zip_files/"
# IOT_DATASET_META["is_dir"] = False


def main():
    """Test using Reinforcement Learning to extract Decision Tree from a generic Blackbox model"""
    logger = log.Logger(
        "{}/trust_report_{}.log".format(
            OUTPUT_PATH,
            "RandomForestClassifier",
        )
    )

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
    logger.log("Done!")

    logger.log("Initializing model: {}...".format("RandomForestClassifier"))
    blackbox = RandomForestClassifier(n_jobs=4)
    # blackbox.fit(X_train, y_train if isinstance(y_train, pd.DataFrame) else y_train.ravel())

    clf = DecisionTreeClassifier(random_state=0)
    path = clf.cost_complexity_pruning_path(X, y)
    ccp_alphas, impurities = path.ccp_alphas, path.impurities
    dagger_ccp_alpha = 0.0

    for ccp, gini in zip(ccp_alphas, impurities):
        # find largest ccp with up to 0.1 impurity
        if gini <= 0.1 and ccp > dagger_ccp_alpha:
            dagger_ccp_alpha = ccp

    trust_report(
        blackbox,
        X=X,
        y=y,
        logger=logger,
        max_iter=1,
        dagger_num_iter=1,
        dagger_ccp_alpha=dagger_ccp_alpha,
        output="{}/dt_trust_report".format(OUTPUT_PATH),
        feature_names=feature_names,
        class_names=IOT_DATASET_META["classes"],
    )


if __name__ == "__main__":
    main()
