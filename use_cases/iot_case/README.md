# IoT Use Case

Trustee application to Random Forest Classifier to distguish IoT devices [[1]](#references), trained with features extracted from the pcaps from the UNSW IoT Dataset [[2]](#references)                             

## Reproducibility steps

Use case was developed and executed in Linux Ubuntu 20.04 and in MacOS Monterey 12.3, running Python 3.7.
The steps below, however, mostly apply to Linux Ubuntu (especially installing requirements), but similar steps aplly to MacOS.


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
cd emperor/use_cases/iot_case/
```

### Run use case code

1. Install Python dependencies
```
poetry install
```

2. Activate Python virtual environment 
```
poetry shell
```

3. Run Trust Report
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
cd emperor/use_cases/iot_case/
```

### Run use case 

1. Build Docker image
```
docker build . -t emperor-iot
```

2. Run use case inside docker container
```
docker run -it --name emperor-iot -v /<path_to_repository>/emperor/use_cases/iot_case/res:/emperor/res/ emperor-iot python main.py 
```

### Check results

The results of the Truste Report and Trustee can be found at the `./res/output/` directory.

## References

[1] Z. Xiong and N. Zilberman. Do Switches Dream of Machine Learning? Toward In-Network Classification. In Proceedings of the 18th ACM Workshop on Hot Topics in Networks, HotNets ’19, page 25–33, New York, NY, USA, 2019. Association for Computing Machinery.<br>
[2] A. Sivanathan, H. H. Gharakheili, F. Loi, A. Radford, C. Wijenayake, A. Vishwanath, and V. Sivaraman. Classifying IoT Devices in Smart Environments Using Network Traffic Characteristics. IEEE Transactions on Mobile Computing, 18(8):1745–1759, 2019.<br>