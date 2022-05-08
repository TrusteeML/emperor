# nPrint dataset
We used preprocessed version of CIC-IDS-2017 dataset, as per the nPrint paper. 
You can download this dataset from https://nprint.github.io/datasets.html.

Direct link: https://drive.google.com/drive/folders/158Lwb9TwopIJ0lGPuFik5744qPiqrg9F,
folder "netml case studies", subfolder "ids".

## How to prepare the dataset
- Step 1: Download and ungzip the 100-packet-traffic.pcapng.gz
- Step 2: use pcapml to separate the file to flows
  - `pcapml -M 100-packet-traffic.pcapng -O output_dir_name/`
