# VIPER

The code provided has been tested on Ubuntu 20.04 with python3.7. 
We recommend using Docker and `conda` environment 
for the installation.

## 1. Install system-wide libraries
```shell
apt install graphviz libopencv-dev python3-opencv
```

##2. Install VIPER requirements
Disclaimer: the original repo has not provided exact packages versions or requirements file.
We reproduced the environment according to our understanding and knowledge.
```shell
pip install -r requirements.txt
```

##3. Install scikit-explain
```shell
#TODO: add
```

##4. Reproduce VIPER results
```shell
cd viper/python
python -m viper.pong.main
```

##5. Reproduce Emperor results with the same model
```shell
mkdir results
python emperor_main.py --model viper/data/model-atari-pong-1/saved --output_dir results
```