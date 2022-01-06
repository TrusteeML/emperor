import os

import pandas as pd
import matplotlib.pyplot as plt
from pandas.core.reshape.merge import merge

LABELS_INFO = "../labels-os.txt"
DATASET_INFO = "../dataset_info.csv"
PLOTS_DIR = "../plots"


def plot_unique_count(df, column):
    if column != "src_ip":
        filtered_df = df.filter(["src_ip", column])
        ax = filtered_df.groupby(column).count().plot.bar(grid=False)
    else:
        ax = df[column].value_counts().plot(kind="bar", grid=False)

    ax.tick_params(axis='both', labelsize=6)
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
    ax.tick_params(axis='both', labelsize=6)
    plt.savefig("{}/total/cdf/{}_cdf_bar.pdf".format(PLOTS_DIR, column))
    plt.close()

    ax = stats_df.plot(x=column, y=["pdf", "cdf"], grid=False)
    ax.tick_params(axis='both', labelsize=6)
    plt.savefig("{}/total/cdf/{}_cdf_line.pdf".format(PLOTS_DIR, column))
    plt.close()
    

def plot_hist(df, column, by=None):
    if by:
        df.hist(column=column, grid=False, by=by)
        plt.savefig("{}/by-os/hist/{}_hist.pdf".format(PLOTS_DIR, column))
    else:
        ax = df[column].hist(grid=False, by=by)
        ax.tick_params(axis='both', labelsize=6)
        plt.savefig("{}/total/hist/{}_hist.pdf".format(PLOTS_DIR, column))
    plt.close()


def plot_dataset():
    print("Reading dataset info file...")
    df = pd.read_csv(DATASET_INFO)
    print(df)
    for column in df.columns:
        if column != 'SACK' and column != 'TIMESTAMP':
            print('Column:', column)
            if column == 'window_size':
                df = df.loc[df['flags_syn'] == 1]

            plot_unique_count(df, column)
            plot_hist(df, column)
            plot_cdf(df, column)


def plot_unique_by_os(df):
    split_dfs = [x for _, x in df.groupby('label')]
    for column in df.columns:
        if column == 'ttl' or column == 'data_offset' or column == 'window_size' or column == 'WINDOW_SCALING':
            print('Column:', column)
            for count, split_df in enumerate(split_dfs):
                if column == 'window_size':
                    split_df = split_df.loc[split_df['flags_syn'] == 1]
                    
                plt.subplot(2, 2, count + 1)
                filtered_df = split_df.filter(["src_ip", column])
                ax = filtered_df.groupby(column).count().plot.bar(grid=False, ax=plt.gca())

                ax.tick_params(axis='both', labelsize=6)
                ax.set_title(split_df['label'].unique()[0], fontsize=8)

            plt.tight_layout()
            plt.savefig("{}/by-os/unique/{}_unique.pdf".format(PLOTS_DIR, column))
            plt.close()


def plot_cdf_by_os(df):
    split_dfs = [x for _, x in df.groupby('label')]
    for column in df.columns:
        if column == 'ttl' or column == 'data_offset' or column == 'window_size' or column == 'WINDOW_SCALING':
            print('Column:', column)
            for count, split_df in enumerate(split_dfs):
                if column == 'window_size':
                    split_df = split_df.loc[split_df['flags_syn'] == 1]

                plt.subplot(2, 2, count + 1)
                rename_dict = {}
                rename_dict[column] = "frequency"
                stats_df = split_df.groupby(column)[column].agg("count").pipe(pd.DataFrame).rename(columns=rename_dict)
                # PDF
                stats_df["pdf"] = stats_df["frequency"] / sum(stats_df["frequency"])
                # CDF
                stats_df["cdf"] = stats_df["pdf"].cumsum()
                stats_df = stats_df.reset_index()
                ax = stats_df.plot.bar(x=column, y=["pdf", "cdf"], grid=False, ax=plt.gca())
                ax.tick_params(axis='both', labelsize=6)
                ax.set_title(split_df['label'].unique()[0], fontsize=8)

            plt.tight_layout()
            plt.savefig("{}/by-os/cdf/{}_cdf_bar.pdf".format(PLOTS_DIR, column))
            plt.close()

            for count, split_df in enumerate(split_dfs):
                if column == 'window_size':
                    split_df = split_df.loc[split_df['flags_syn'] == 1]
                plt.subplot(2, 2, count + 1)
                rename_dict = {}
                rename_dict[column] = "frequency"
                stats_df = split_df.groupby(column)[column].agg("count").pipe(pd.DataFrame).rename(columns=rename_dict)
                # PDF
                stats_df["pdf"] = stats_df["frequency"] / sum(stats_df["frequency"])
                # CDF
                stats_df["cdf"] = stats_df["pdf"].cumsum()
                stats_df = stats_df.reset_index()
                ax = stats_df.plot(x=column, y=["pdf", "cdf"], grid=False, ax=plt.gca())
                ax.tick_params(axis='both', labelsize=6)
                ax.set_title(split_df['label'].unique()[0], fontsize=8)

            plt.tight_layout()
            plt.savefig("{}/by-os/cdf/{}_cdf_line.pdf".format(PLOTS_DIR, column))
            plt.close()


def plot_dataset_by_os():
    print("Reading dataset info file...")
    df = pd.read_csv(DATASET_INFO)
    labels = pd.read_csv(LABELS_INFO)
    merged = pd.merge(df, labels, left_on="src_ip", right_on="item")
    # dst_merged = pd.merge(df, labels, left_on="dst_ip", right_on="item")
    # merged = pd.concat([src_merged, dst_merged])
    print(merged)

    for column in merged.columns:
        if column != 'label' and column != 'SACK' and column != 'TIMESTAMP':
            print('Column:', column)
            if column == 'window_size':
                df = merged.loc[merged["flags_syn"] == 1]
                plot_hist(df, column, by='label')
            else:
                plot_hist(merged, column, by='label')

    plot_unique_by_os(merged)
    plot_cdf_by_os(merged)


if __name__ == "__main__":
    if not os.path.exists("{}/total/hist/".format(PLOTS_DIR)):
        os.makedirs("{}/total/hist/".format(PLOTS_DIR))
    if not os.path.exists("{}/total/cdf/".format(PLOTS_DIR)):
        os.makedirs("{}/total/cdf/".format(PLOTS_DIR))
    if not os.path.exists("{}/total/unique/".format(PLOTS_DIR)):
        os.makedirs("{}/total/unique/".format(PLOTS_DIR))

    if not os.path.exists("{}/by-os/cdf/".format(PLOTS_DIR)):
        os.makedirs("{}/by-os/cdf/".format(PLOTS_DIR))
    if not os.path.exists("{}/by-os/unique/".format(PLOTS_DIR)):
        os.makedirs("{}/by-os/unique/".format(PLOTS_DIR))
    if not os.path.exists("{}/by-os/hist/".format(PLOTS_DIR)):
        os.makedirs("{}/by-os/hist/".format(PLOTS_DIR))

    plot_dataset()
    plot_dataset_by_os()
