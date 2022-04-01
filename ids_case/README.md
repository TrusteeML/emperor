2 cases:  
1. Train on big dataset with only tcpoptions, show the f1-score and
create a decision tree to visualize
   1. Ensure that nprint_dataset is downloaded and prepared (see `res/nprint_dataset/README.md`)
   2. Modify `res/run-nprint-tcpoptions-only.sh` to specify label filename, pcap folder location and model output location
   3. Run `res/run-nprint-tcpoptions-only.sh`
2. Train on big dataset with all options except ip addresses, 
check on the campus dataset, show f-1 score,
confusion matrix, and visualize the tree
   1. Ensure that nprint_dataset is downloaded and prepared (see `res/nprint_dataset/README.md`)
   2. Ensure that campus_dataset is prepared (see `res/campus_dataset/README.md`)
   3. Run `res/run-nprint-campus-comparison.sh`
   4. Run `./campus-comparison.py`