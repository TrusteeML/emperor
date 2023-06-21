# Heartbleed Use Case

 Trustee application to a Random Forest Classifier for an Intrustion Detection System, <br>trained with CIC-IDS-2017 dataset pre-computed features [[1]](#references)                         

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
cd emperor/use_cases/heartbleed_case/
```


### Run use case 

1. Install Python dependencies (resolving dependencies can take a while)
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

4. Run validation test with o.o.d. Heartbleed samples
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
git clone git@github.com:asjacobs92/emperor.git
cd emperor/use_cases/heartbleed_case/
```

### Run use case 

1. Run Makefile to build and run code in a Docker container
```
make
```

OR

1. Build Docker image
```
docker build . -t emperor-heartbleed
```

1. Run use case inside docker container
```
docker run -it --name emperor-heartbleed -v /<path_to_repository>/emperor/use_cases/heartbleed_case/res:/emperor/res/ emperor-heartbleed python main.py 
```

### Check results

The results of the Truste Report and Trustee can be found at the `./res/output/` directory.

## References

[1] I. Sharafaldin., A. H. Lashkari., and A. A. Ghorbani. Toward Gener- ating a New Intrusion Detection Dataset and Intrusion Traffic Characterization. In Proceedings of the 4th International Conference on Information Systems Security and Privacy - ICISSP, pages 108–116. INSTICC, SciTePress, 2018.<br>