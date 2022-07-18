import os
import shutil
import pandas as pd


NPTS_PATH = "full_model/nprint/"
SUB_NPTS_PATH = "nprintml/sub_nprint/"
LABELS_PATH = "labels.txt"
SUB_LABELS_PATH = "sub_labels.txt"


def main():
    """Reads pcap list from labels file and subsamples the dataframe."""
    if not os.path.exists(SUB_NPTS_PATH):
        os.makedirs(SUB_NPTS_PATH)

    df = pd.read_csv(LABELS_PATH, header=0)
    df = df.groupby("label").head(5000).reset_index(drop=True)
    df.to_csv(SUB_LABELS_PATH, header=True, index=False)
    df.apply(lambda x: shutil.copy(f"{NPTS_PATH}{x['item'].replace('pcap', 'npt')}", SUB_NPTS_PATH), axis=1)


if __name__ == "__main__":
    main()
