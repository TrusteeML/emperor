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
We reproduced the environment according to our understanding and knowledge. We used `poetry` for dependencies tracking.
```shell
poetry init
```

##3. Install scikit-explain
```shell
#TODO: add
```

##4. Reproduce VIPER results
```shell
mkdir results
cd viper/python
python -m viper.pong.main
cp tmp/dt_output.dot ../../results/viper_dt.dot
cd ../..
```

##5. Reproduce Emperor results with the same model
```shell
python emperor_main.py --model viper/data/model-atari-pong-1/saved --output_dir results
```
