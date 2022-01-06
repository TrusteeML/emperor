import os

import pandas as pd
import matplotlib.pyplot as plt
from pandas.core.reshape.merge import merge

LABELS_INFO = "../labels.txt"
DATASET_INFO = "../dataset_info.csv"
PLOTS_DIR = "../plots"


def plot_unique_count(df, column):
    if column != "src_ip":
        filtered_df = df.filter(["src_ip", column])
        ax = filtered_df.groupby(column).count().plot.bar(grid=False)
    else:
        ax = df[column].value_counts().plot(kind="bar", grid=False)

    ax.tick_params(axis="both", labelsize=6)
    plt.savefig("{}/total/unique/{}_unique.pdf".format(PLOTS_DIR, column))
    plt.close()


def plot_cdf(df, column):
    rename_dict = {}
    rename_dict[column] = "frequency"
    stats_df = df.groupby(column)[column].agg("count").pipe(pd.DataFrame).rename(columns=rename_dict)

    # PDF
    stats_df["pdf"] = stats_df["frequency"] / sum(stats_df["frequency"])

    # CDF
    stats_df["cdf"] = stats_df["pdf"].cumsum()
    stats_df = stats_df.reset_index()

    ax = stats_df.plot.bar(x=column, y=["pdf", "cdf"], grid=False)
    ax.tick_params(axis="both", labelsize=6)
    plt.savefig("{}/total/cdf/{}_cdf_bar.pdf".format(PLOTS_DIR, column))
    plt.close()

    ax = stats_df.plot(x=column, y=["pdf", "cdf"], grid=False)
    ax.tick_params(axis="both", labelsize=6)
    plt.savefig("{}/total/cdf/{}_cdf_line.pdf".format(PLOTS_DIR, column))
    plt.close()


def plot_hist(df, column, by=None):
    if by:
        df.hist(column=column, grid=False, by=by)
        plt.tight_layout()
        plt.savefig("{}/by-class/hist/{}_hist.pdf".format(PLOTS_DIR, column))
    else:
        ax = df[column].hist(grid=False, by=by)
        ax.tick_params(axis="both", labelsize=6)
        plt.savefig("{}/total/hist/{}_hist.pdf".format(PLOTS_DIR, column))
    plt.close()


def plot_unique_by_label(df):
    split_dfs = [x for _, x in df.groupby("label")]
    for column in df.columns:
        if column != "src_ip" or column == "dst_ip":
            print("Column:", column)
            for count, split_df in enumerate(split_dfs):
                if column == "window_size":
                    split_df = split_df.loc[split_df["flags_syn"] == 1]

                plt.subplot(3, 3, count + 1)
                filtered_df = split_df.filter(["src_ip", column])
                ax = filtered_df.groupby(column).count().plot.bar(grid=False, ax=plt.gca())

                ax.tick_params(axis="both", labelsize=6)
                ax.set_title(split_df["label"].unique()[0], fontsize=8)

            plt.tight_layout()
            plt.savefig("{}/by-class/unique/{}_unique.pdf".format(PLOTS_DIR, column))
            plt.close()


def plot_cdf_by_label(df):
    split_dfs = [x for _, x in df.groupby("label")]
    for column in df.columns:
        if column != "src_ip" or column == "dst_ip":
            print("Column:", column)
            for count, split_df in enumerate(split_dfs):
                if column == "window_size":
                    split_df = split_df.loc[split_df["flags_syn"] == 1]

                plt.subplot(3, 3, count + 1)
                rename_dict = {}
                rename_dict[column] = "frequency"
                stats_df = split_df.groupby(column)[column].agg("count").pipe(pd.DataFrame).rename(columns=rename_dict)
                # PDF
                stats_df["pdf"] = stats_df["frequency"] / sum(stats_df["frequency"])
                # CDF
                stats_df["cdf"] = stats_df["pdf"].cumsum()
                stats_df = stats_df.reset_index()
                ax = stats_df.plot.bar(x=column, y=["pdf", "cdf"], grid=False, ax=plt.gca())
                ax.tick_params(axis="both", labelsize=6)
                ax.set_title(split_df["label"].unique()[0], fontsize=8)

            plt.tight_layout()
            plt.savefig("{}/by-class/cdf/{}_cdf_bar.pdf".format(PLOTS_DIR, column))
            plt.close()

            for count, split_df in enumerate(split_dfs):
                if column == "window_size":
                    split_df = split_df.loc[split_df["flags_syn"] == 1]
                plt.subplot(3, 3, count + 1)
                rename_dict = {}
                rename_dict[column] = "frequency"
                stats_df = split_df.groupby(column)[column].agg("count").pipe(pd.DataFrame).rename(columns=rename_dict)
                # PDF
                stats_df["pdf"] = stats_df["frequency"] / sum(stats_df["frequency"])
                # CDF
                stats_df["cdf"] = stats_df["pdf"].cumsum()
                stats_df = stats_df.reset_index()
                ax = stats_df.plot(x=column, y=["pdf", "cdf"], grid=False, ax=plt.gca())
                ax.tick_params(axis="both", labelsize=6)
                ax.set_title(split_df["label"].unique()[0], fontsize=8)

            plt.tight_layout()
            plt.savefig("{}/by-class/cdf/{}_cdf_line.pdf".format(PLOTS_DIR, column))
            plt.close()


def plot_dataset_by_label():
    print("Reading dataset info file...")
    df = pd.read_csv(DATASET_INFO)
    print(df)
    labels = pd.read_csv(LABELS_INFO)
    # split = labels["item"].str.split("-", expand=True)
    labels[["label_orig", "label_orig_spec", "src_ip", "dst_ip", "src_prt", "dst_prt", "protocol", "pcap_id"]] = labels["item"].str.split(
        "-", expand=True
    )
    labels["src_prt"] = labels["src_prt"].astype("int64")
    labels["dst_prt"] = labels["dst_prt"].astype("int64")
    labels["protocol"] = labels["protocol"].str.upper()
    print(labels)
    merged = pd.merge(df, labels, on=["src_ip", "dst_ip", "src_prt", "dst_prt", "protocol"])
    print(merged)
    merged = merged.drop(columns=["item", "label_orig", "label_orig_spec", "pcap_id", "SACK", "TIMESTAMP"])

    for column in merged.columns:
        if column != "label":
            print("Column:", column)
            if column == "window_size":
                df = merged.loc[merged["flags_syn"] == 1]
                plot_hist(df, column, by="label")
            else:
                plot_hist(merged, column, by="label")

    plot_unique_by_label(merged)
    plot_cdf_by_label(merged)


def plot_dataset():
    print("Reading dataset info file...")
    df = pd.read_csv(DATASET_INFO)
    print(df)
    labels = pd.read_csv(LABELS_INFO)
    # split = labels["item"].str.split("-", expand=True)
    labels[["label_orig", "label_orig_spec", "src_ip", "dst_ip", "src_prt", "dst_prt", "protocol", "pcap_id"]] = labels["item"].str.split(
        "-", expand=True
    )
    labels["src_prt"] = labels["src_prt"].astype("int64")
    labels["dst_prt"] = labels["dst_prt"].astype("int64")
    labels["protocol"] = labels["protocol"].str.upper()
    print(labels)
    merged = pd.merge(df, labels, on=["src_ip", "dst_ip", "src_prt", "dst_prt", "protocol"])
    print(merged)
    merged = merged.drop(columns=["item", "label_orig", "label_orig_spec", "pcap_id", "SACK", "TIMESTAMP"])

    for column in merged.columns:
        print("Column:", column)
        if column == "window_size":
            merged = merged.loc[merged["flags_syn"] == 1]

        plot_unique_count(merged, column)
        plot_hist(merged, column)
        plot_cdf(merged, column)


if __name__ == "__main__":
    if not os.path.exists("{}/total/hist/".format(PLOTS_DIR)):
        os.makedirs("{}/total/hist/".format(PLOTS_DIR))
    if not os.path.exists("{}/total/cdf/".format(PLOTS_DIR)):
        os.makedirs("{}/total/cdf/".format(PLOTS_DIR))
    if not os.path.exists("{}/total/unique/".format(PLOTS_DIR)):
        os.makedirs("{}/total/unique/".format(PLOTS_DIR))

    if not os.path.exists("{}/by-class/cdf/".format(PLOTS_DIR)):
        os.makedirs("{}/by-class/cdf/".format(PLOTS_DIR))
    if not os.path.exists("{}/by-class/unique/".format(PLOTS_DIR)):
        os.makedirs("{}/by-class/unique/".format(PLOTS_DIR))
    if not os.path.exists("{}/by-class/hist/".format(PLOTS_DIR)):
        os.makedirs("{}/by-class/hist/".format(PLOTS_DIR))

    # plot_dataset()
    plot_dataset_by_label()
