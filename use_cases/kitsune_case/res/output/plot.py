import pandas as pd
import matplotlib.pyplot as plt

from matplotlib import rcParams

FONT_NAME = "Roboto"
FONT_WEIGHT = "light"

rcParams["font.family"] = "serif"
rcParams["font.serif"] = [FONT_NAME]
rcParams["font.weight"] = FONT_WEIGHT

MIRAI_TAMPERED_50_90_PATH = "mirai_tampered_50-90.csv"
MIRAI_TAMPERED_30_70_PATH = "mirai_tampered_30-70.csv"
MIRAI_TAMPERED_10_50_PATH = "mirai_tampered_10-50.csv"
MIRAI_TAMPERED_ATTACK_PATH = "mirai_tampered_attack_only.csv"
MIRAI_PATH = "mirai.csv"

MAX_SAMPLES = 200000
FMgrace = 5000  # the number of instances taken to learn the feature mapping (the ensemble's architecture)
ADgrace = 50000  # the number of instances used to train the anomaly detector (ensemble itself)
TRAINING_SAMPLES = FMgrace + ADgrace + 1


def main():
    """Plot Kitsune outputs for different mirai pcaps"""
    mirai_df = pd.read_csv(MIRAI_PATH, header=0)
    mirai_tampered_10_50_df = pd.read_csv(MIRAI_TAMPERED_10_50_PATH, header=0)
    mirai_tampered_30_70_df = pd.read_csv(MIRAI_TAMPERED_30_70_PATH, header=0)
    mirai_tampered_50_90_df = pd.read_csv(MIRAI_TAMPERED_50_90_PATH, header=0)

    results = [
        mirai_df["rmse"][TRAINING_SAMPLES:MAX_SAMPLES],
        mirai_tampered_50_90_df["rmse"][TRAINING_SAMPLES:MAX_SAMPLES],
        mirai_tampered_30_70_df["rmse"][TRAINING_SAMPLES:MAX_SAMPLES],
        mirai_tampered_10_50_df["rmse"][TRAINING_SAMPLES:MAX_SAMPLES],
    ]
    labels = [
        "Original",
        "Tampered 50-90",
        "Tampered 30-70",
        "Tampered 10-50",
    ]
    print(results)

    colors = [
        "#d75d5b",
        "#a7c3cd",
        "#8a4444",
        "#c8c5c3",
        "#524a47",
        "#f5f0ed",
        "#edeef0",
    ]

    print("Plotting results")
    plt.figure(figsize=(4, 3))
    x = range(0, len(mirai_df["rmse"][TRAINING_SAMPLES:MAX_SAMPLES]))
    for idx, y in enumerate(results):
        plt.scatter(
            x,
            y,
            color=colors[idx] if idx < len(colors) else None,
            label=labels[idx] if idx < len(labels) else "",
        )
    plt.xlim(TRAINING_SAMPLES, len(x) + 10000)
    plt.ylim(0, 20)
    plt.legend()
    plt.ylabel("RMSE", fontsize=12, fontname=FONT_NAME, fontweight=FONT_WEIGHT)
    plt.xlabel(
        "Number of packets", fontsize=12, fontname=FONT_NAME, fontweight=FONT_WEIGHT
    )
    plt.tight_layout()
    plt.savefig("results.png", dpi=600)
    plt.close()

    plt.figure(figsize=(4, 3))
    original_results = results[0]
    plt.plot(
        original_results,
        original_results,
        color=colors[0],
        label="Original results",
    )
    for idx, y in enumerate(results[1:]):
        plt.scatter(
            original_results,
            y,
            color=colors[idx + 1] if idx + 1 < len(colors) else None,
            label=labels[idx + 1] if idx + 1 < len(labels) else "",
        )
    plt.ylim(0, 16)
    plt.xlim(0, 16)
    plt.legend()
    plt.ylabel(
        "Predicted RMSE", fontsize=12, fontname=FONT_NAME, fontweight=FONT_WEIGHT
    )
    plt.xlabel("Expected RMSE", fontsize=12, fontname=FONT_NAME, fontweight=FONT_WEIGHT)
    plt.tight_layout()
    plt.savefig("rmse_results.png", dpi=600)
    plt.close()


if __name__ == "__main__":
    main()
