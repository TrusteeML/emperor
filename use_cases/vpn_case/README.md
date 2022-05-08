# IoT Use Case

Trustee application the 1D-CNN trained to detect VPN traffic from [[1]](#references),<br> trained with the ISCX VPN-nonVPN dataset [[2]](#references)

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
git clone git@github.com:anon4papers/emperor.git
cd emperor/use_cases/vpn_case/
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

3. Run byte tempering validation
```
python validation.py 
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
git clone git@github.com:anon4papers/emperor.git
cd emperor/use_cases/vpn_case/
```

### Run use case 

1. Build Docker image
```
docker build . -t emperor-vpn
```

2. Run use case inside docker container
```
docker run -it --name emperor-vpn -v /<path_to_repository>/emperor/use_cases/vpn_case/res:/emperor/res/ emperor-vpn python main.py 
```

### Check results

The results of the Truste Report and Trustee can be found at the `./res/output/` directory.

## References

[1] W. Wang, M. Zhu, J. Wang, X. Zeng, and Z. Yang. End-to-end encrypted traffic classification with one-dimensional convolution neural networks. In 2017 IEEE International Conference on Intelligence and Security Informatics (ISI), pages 43–48, 2017. Code available at GitHub repository https://github.com/echowei/DeepTraffic.<br>
[2] G. Draper-Gil., A. H. Lashkari., M. S. I. Mamun, and A. A. Ghorbani. Characterization of Encrypted and VPN Traffic using Time-related Features. In Proceedings of the 2nd International Conference on Information Systems Security and Privacy - ICISSP,, pages 407–414. INSTICC, SciTePress, 2016.<br>