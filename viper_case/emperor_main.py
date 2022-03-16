import argparse
import graphviz
import numpy as np

from sklearn import tree
from sklearn.metrics import classification_report, f1_score

from viper.python.viper.pong.dqn import DQNPolicy
from viper.python.viper.pong.pong import get_pong_symbolic, get_pong_env
from viper.python.viper.core.rl import get_rollouts, test_policy

from skexplain.utils import log
from skexplain.imitation import Dagger


N_ROLLOUTS = 150  # 80 * (10+1)    # the same amount of total rollouts as viper: n_batch_rollouts * (max_iters + 1 (initial))


class CustomDecisionTreeClassifier(tree.DecisionTreeClassifier):
    """
    Since original VIPER uses different X form for teacher and student in order to work with unified Dagger we will
    introduce custom classifier which preprocesses the data for every predict and fit call
    """
    def __init__(self, *args, **kwargs):
        self.input_transformer = get_pong_symbolic
        super().__init__(*args, **kwargs)

    def _apply_transformer(self, X):
        return np.array([self.input_transformer(X[i, ...]) for i in range(X.shape[0])])

    def predict(self, X, check_input=True):
        return super().predict(self._apply_transformer(X), check_input)

    def fit(self, X, y, sample_weight=None, check_input=True, X_idx_sorted="deprecated"):
        return super().fit(self._apply_transformer(X), y, sample_weight, check_input, X_idx_sorted)


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--model", type=str, default="viper/data/model-atari-pong-1/saved", help="VIPER model checkpoint folder")
    parser.add_argument("--output_dir", type=str, default="results", help="Output folder for results")
    args = parser.parse_args()
    MODEL_PATH = args.model
    OUTPUT_DIR = args.output_dir

    logger = log.Logger(f"{OUTPUT_DIR}/emperor_pong.log")

    env = get_pong_env()
    teacher = DQNPolicy(env, MODEL_PATH)

    logger.log(f"Evaluating teacher model in the environment...")
    rew = test_policy(env, teacher, state_transformer=lambda x: x, n_test_rollouts=10)
    logger.log(f"Done!")
    logger.log(f"Average reward: {rew}")

    logger.log(f"Generating rollouts from the environment {env}...")

    obss = []
    acts = []
    trace = get_rollouts(env, teacher, False, N_ROLLOUTS)
    obss.extend((obs for obs, _, _ in trace))
    acts.extend((act for _, act, _ in trace))

    Xs = np.array(obss)
    ys = np.array(acts)
    logger.log(f"X size: {len(Xs)}; y size: {len(ys)}")
    logger.log("Done!")

    logger.log("Using Classification Dagger algorithm to extract DT...")

    # Again, here we construct Dagger manually only because different state representations are used for teacher and student models
    dagger = Dagger(expert=teacher, student_class=CustomDecisionTreeClassifier, logger=logger)
    dagger.score = lambda y_true, y_pred, average="macro": f1_score(y_true, y_pred, average=average)

    dagger.fit(
        Xs,
        ys,
        num_samples=200000,
        num_iter=40,
        verbose=True
    )

    logger.log("#" * 10, "Explanation validation", "#" * 10)
    (dt, reward, idx) = dagger.explain()
    logger.log("Model explanation {} local fidelity: {}".format(idx, reward))


    # generate new data for report
    obss = []
    acts = []
    trace = get_rollouts(env, teacher, False, N_ROLLOUTS)
    obss.extend((obs for obs, _, _ in trace))
    acts.extend((act for _, act, _ in trace))

    Xs = np.array(obss)
    ys = np.array(acts)

    dt_y_pred = dt.predict(Xs)

    logger.log("Model explanation global fidelity report:")
    logger.log(
        "\n{}".format(
            classification_report(
                ys,
                dt_y_pred,
                digits=3,
            )
        )
    )

    logger.log("Evaluating student model in the environment...")
    # Here we introduce state transformer as a do-nothing-function as dt is our CustomDecisionTreeClassifier with
    # state_transformer already implemented (and we want to use VIPER's function where it's possible)
    rew = test_policy(env, dt, state_transformer=lambda x: x, n_test_rollouts=10)
    logger.log(f"Done!")
    logger.log(f"Average reward: {rew}")

    logger.log(f"Exporting tree visualization to {OUTPUT_DIR}...")
    dot_data = tree.export_graphviz(dt, filled=True, rounded=True, special_characters=True)
    graph = graphviz.Source(dot_data)
    graph.render("{}/dt_{}_{}_{}".format(OUTPUT_DIR, "TabularPredictor", "dagger", dt.get_n_leaves()))
    logger.log("Done!")


if __name__ == '__main__':
    main()
