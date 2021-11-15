import pandas as pd
import matplotlib.pyplot as plt

LABELS_INFO = "labels-os.txt"
DATASET_INFO = "dataset_info.csv"
PLOTS_DIR = "plots"


def plot_unique_count(df, column):
    if column != "src_ip":
        filtered_df = df.filter(["src_ip", column])
        filtered_df.groupby(column).count().plot.bar()
        # ax = df["ttl"].sort_index().value_counts(sort=False).plot(kind="bar", figsize=(14, 8))
        # ax.set_xlabel("TTL Value")
        # ax.set_ylabel("Frequency")
        # plt.xticks(range(-1, 256, 20))
    else:
        df[column].value_counts().plot(kind="bar")

    plt.savefig("{}/{}_unique.pdf".format(PLOTS_DIR, column))


def plot_cdf(df, column):
    rename_dict = {}
    rename_dict[column] = "frequency"
    stats_df = df.groupby(column)[column].agg("count").pipe(pd.DataFrame).rename(columns=rename_dict)

    # PDF
    stats_df["pdf"] = stats_df["frequency"] / sum(stats_df["frequency"])

    # CDF
    stats_df["cdf"] = stats_df["pdf"].cumsum()
    stats_df = stats_df.reset_index()

    stats_df.plot.bar(x=column, y=["pdf", "cdf"], grid=True)
    plt.savefig("{}/{}_cdf.pdf".format(PLOTS_DIR, column))


def plot_hist(df, column):
    df[column].hist()
    plt.savefig("{}/{}_hist.pdf".format(PLOTS_DIR, column))


def plot_dataset():
    print("Reading dataset info file...")
    df = pd.read_csv(DATASET_INFO)
    print(df)
    for column in df.columns:
        # plot_unique_count(df, column)
        # plot_hist(df, column)
        plot_cdf(df, column)


def plot_dataset_by_os():
    print("Reading dataset info file...")
    df = pd.read_csv(DATASET_INFO)
    print(df)
    labels = pd.read_csv(LABELS_INFO)
    print(labels)
    merged = pd.merge(df, labels, left_on="src_ip", right_on="item")
    print(merged)


if __name__ == "__main__":
    plot_dataset()
    # plot_dataset_by_os()
