import os
import numpy as np

from skexplain.report import TrustReport
from skexplain.utils import dataset, log, persist
from skexplain.utils.const import CIC_IDS_2017_DATASET_META

from sklearn.ensemble import RandomForestClassifier
from sklearn.metrics import classification_report
from sklearn.model_selection import train_test_split


DF_PATH = "res/dataset/CIC-IDS-2017/"
DF_OVER_PATH = "res/dataset/CIC-IDS-2017_OverSampled.csv.zip"
DF_OVER_MIN_PATH = "res/dataset/CIC-IDS-2017_OverSampled_min.csv.zip"
DF_VALIDATE_PATH = "res/dataset/validation/heartbleed.csv"
MODEL_PATH = "res/models/RandomForestClassifier_cic_ids_2017.joblib.zip"

OUTPUT_PATH = "res/output"
REPORT_PATH = f"{OUTPUT_PATH}/report/trust_report.obj"

# if using oversampled df
CIC_IDS_2017_DATASET_META["is_dir"] = False


def main():
    logger = log.Logger("{}/output.log".format(OUTPUT_PATH))

    if os.path.exists(REPORT_PATH):
        logger.log(f"Loading trust report from {REPORT_PATH}...")
        trust_report = TrustReport.load(REPORT_PATH)
        logger.log("Done!")
    else:
        logger.log("Reading CIC-IDS-2017 dataset...")
        # Step 1: Parse train-test def
        X, y, feature_names, _, _ = dataset.read(
            DF_OVER_MIN_PATH, metadata=CIC_IDS_2017_DATASET_META, as_df=True, verbose=True
        )
        logger.log("Done!")

        # X_indexes = np.arange(0, X.shape[0])
        # X_idx, _, y, _ = train_test_split(X_indexes, y, train_size=0.5, stratify=y)
        # X = X.iloc[X_idx]

        logger.log("Splitting dataset into training and test...")
        X_indexes = np.arange(0, X.shape[0])
        X_train, X_test, y_train, y_test = train_test_split(X_indexes, y, train_size=0.7, stratify=y)
        X_train = X.iloc[X_train]
        X_test = X.iloc[X_test]
        logger.log("Done!")

        # Step 2: Train black-box model with loaded dataset
        logger.log("#" * 10, "Model init", "#" * 10)
        logger.log(f"Looking for pre-trained model: {MODEL_PATH}...")
        blackbox = persist.load_model(MODEL_PATH)
        if not blackbox:
            logger.log("Training model: RandomForestClassifier...")
            blackbox = RandomForestClassifier(n_jobs=4)
            blackbox.fit(X_train, y_train)
            persist.save_model(blackbox, MODEL_PATH)

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
        )

        trust_report = TrustReport(
            blackbox,
            X=X,
            y=y,
            logger=logger,
            top_n=10,
            max_iter=1,
            trustee_num_iter=10,
            num_quantiles=20,
            # skip_retrain=True,
            trustee_sample_size=0.3,
            feature_names=feature_names,
            class_names=CIC_IDS_2017_DATASET_META["classes"],
            verbose=True,
        )

    logger.log(trust_report)
    trust_report.save(OUTPUT_PATH)


if __name__ == "__main__":
    main()
    # df_list = []
    # datasets = glob.glob(DF_PATH + "/*.zip")
    # for dataset_path in datasets:
    #     df = pandas.read_csv(dataset_path, header=0).fillna(-1)
    #     df_list.append(df)
    # df = pandas.concat(df_list, axis=0, ignore_index=True)

    # print(df)
    # print(df.columns)
    # print(df.groupby(' Label').count())
