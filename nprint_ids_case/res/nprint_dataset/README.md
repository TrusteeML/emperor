# nPrint dataset
We used preprocessed version of CIC-IDS-2017 dataset, as per the nPrint paper. 
You can download this dataset from https://nprint.github.io/datasets.html.

Direct link: https://drive.google.com/drive/folders/158Lwb9TwopIJ0lGPuFik5744qPiqrg9F,
folder "netml case studies", subfolder "ids".

## How to prepare the dataset
- Step 1: Download and ungzip the traffic.pcapng.gz
- Step 2: use pcapml to separate the file to flows
  - `pcapml -M traffic.pcapng -O output_dir_name/`
- Step 3: create a file with labels for nprintml from flow files
  - Currently, resulting flow file is named like `14745754350413679427_benign_benign.pcap`,
    corresponding label is benign_benign
  - `echo "filename,label" > labels.txt`
  - `ls output_dir_name | awk -F "[_.]" '{print $0","$2"_"$3}' >> labels.txt`