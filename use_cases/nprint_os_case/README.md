# nPrintML IDS Use Case

Trustee application to the nPrintML [[5]](#references) AutoGluon Tabular Predictor [[9]](#references) <br>for OS Fingerprinting, also trained using with pcaps from the CIC-IDS-2017 dataset [[1]](#references)

## Reproducibility steps

Use case was developed and executed in Linux Ubuntu 20.04, running Python 3.7.
In MacOS, however, we were not able to run this use case, as the AutoGluon library would throw a `segmentation fault` error when training a LightGBM model.

### Prerequisites

1. Install [Python 3.7](https://www.python.org/downloads/)
```   
sudo add-apt-repository ppa:deadsnakes/ppa
sudo apt-get install python3.7
```

2. Install [Poetry](https://python-poetry.org/docs/)
```
curl -sSL https://raw.githubusercontent.com/python-poetry/poetry/master/get-poetry.py | python -
```

3. Clone repository and move into use case directory
```
git clone git@github.com:asjacobs92/emperor.git
cd emperor/use_cases/nprint_os_case/
```

4. Train nPrintML model
  1. Ensure that nprint_dataset is downloaded and prepared (see `./res/dataset/README.md`)
  2. Modify `./res/dataset/run-nprint.sh` to specify label filename, pcap folder location and model output location
  3. Run `./res/dataset/run-nprint.sh`


### Run use case code

1. Install Python dependencies (resolving dependencies can take a while)
```
poetry install
```

2. Activate Python virtual environment 
```
poetry shell
```

3. Update `main.py` to point to trained nPrintML model and dataset.

4. Run Trust Report
```
python main.py 
``` 

### Check results

The results of the Truste Report and Trustee can be found at the `./res/output/` directory.


## Running use case with Docker 

We also make a Dockerfile available to build a Linux container and run the use case in it. 
Follow the steps below to reproduce our results using Docker.

### Prerequisites

1. Install [Docker](https://docs.docker.com/engine/install/ubuntu/)
```
sudo apt-get update
sudo apt-get install docker-ce docker-ce-cli containerd.io docker-compose-plugin
```

2. Clone repository and move into use case directory
```
git clone git@github.com:asjacobs92/emperor.git
cd emperor/use_cases/nprint_os_case/
```

3. Train nPrintML model
  1. Ensure that nprint_dataset is downloaded and prepared (see `res/nprint_dataset/README.md`)
  2. Modify `res/run-nprint.sh` to specify label filename, pcap folder location and model output location
  3. Run `res/run-nprint.sh`


### Run use case 

1. Build Docker image
```
docker build . -t emperor-nprint-os
```

2. Run use case inside docker container
```
docker run -it --name emperor-nprint-os -v /<path_to_repository>/emperor/use_cases/nprint_os_case/res:/emperor/res/ emperor-nprint-os python main.py 
```

### Check results

The results of the Truste Report and Trustee can be found at the `./res/output/` directory.

## References

[1] J. Holland, P. Schmitt, N. Feamster, and P. Mittal. New Directions in Automated Traffic Analysis. In Proceedings of the 2021 ACM SIGSAC Conference on Computer and Communications Security, CCS ’21, page 3366–3383, New York, NY, USA, 2021. Association for Computing Machinery.<br>
[2] N. Erickson, J. Mueller, A. Shirkov, H. Zhang, P. Larroy, M. Li, and A. Smola. AutoGluon-Tabular: Robust and Accurate AutoML for Structured Data, 2020.<br>
[3] I. Sharafaldin., A. H. Lashkari., and A. A. Ghorbani. Toward Gener- ating a New Intrusion Detection Dataset and Intrusion Traffic Characterization. In Proceedings of the 4th International Conference on Information Systems Security and Privacy - ICISSP, pages 108–116. INSTICC, SciTePress, 2018.<br>
