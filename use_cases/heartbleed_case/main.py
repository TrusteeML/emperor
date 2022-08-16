import os
import graphviz

from sklearn import tree

from trustee.report import TrustReport
from trustee.utils import dataset, log, persist
from trustee.utils.const import CIC_IDS_2017_DATASET_META


from sklearn.metrics import classification_report
from sklearn.ensemble import RandomForestClassifier


DF_PATH = "res/dataset/CIC-IDS-2017/"
DF_OVER_PATH = "res/dataset/CIC-IDS-2017_OverSampled.csv.zip"
DF_OVER_MIN_PATH = "res/dataset/CIC-IDS-2017_OverSampled_min.csv.zip"
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

        # Step 2: Train black-box model with loaded dataset
        logger.log("#" * 10, "Model init", "#" * 10)
        logger.log(f"Looking for pre-trained model: {MODEL_PATH}...")
        blackbox = persist.load_model(MODEL_PATH)
        if not blackbox:
            blackbox = RandomForestClassifier(n_jobs=4)

        trust_report = TrustReport(
            blackbox,
            X=X,
            y=y,
            logger=logger,
            top_k=10,
            max_iter=10,
            trustee_num_iter=10,
            num_pruning_iter=10,
            trustee_sample_size=0.30,
            analyze_stability=True,
            skip_retrain=False,
            feature_names=feature_names,
            class_names=CIC_IDS_2017_DATASET_META["classes"],
            verbose=True,
        )

        dt_y_pred = trust_report.max_dt.predict(X)
        y_pred = trust_report.blackbox.predict(X)
        logger.log("Explanation classification report will all data:")
        logger.log(f"{classification_report(y, y_pred, digits=3, target_names=CIC_IDS_2017_DATASET_META['classes'])}")
        logger.log("Explanation fidelity report will all data:")
        logger.log(
            f"{classification_report(y_pred, dt_y_pred, digits=3, target_names=CIC_IDS_2017_DATASET_META['classes'])}"
        )

    stable_explanations = trust_report.get_stable_explanations()
    stability_output_dir = f"{OUTPUT_PATH}/stable"
    if not os.path.exists(stability_output_dir):
        os.makedirs(stability_output_dir)

    logger.log("Saving stability decision trees...")
    for idx, it in enumerate(stable_explanations):
        print(it)
        dot_data = tree.export_graphviz(
            it["dt"],
            class_names=CIC_IDS_2017_DATASET_META["classes"],
            feature_names=trust_report.feature_names,
            filled=True,
            rounded=True,
            special_characters=True,
        )
        graph = graphviz.Source(dot_data)
        graph.render(f"{stability_output_dir}/dt_{idx}")

    logger.log(trust_report)
    trust_report.save(OUTPUT_PATH)  # , save_dts=True)


if __name__ == "__main__":
    main()
