FROM python:3.7.17

# just in case
ENV DEBIAN_FRONTEND=noninteractive
SHELL ["/bin/bash", "-c"]

# deps
RUN apt update && apt install -y graphviz fonts-roboto
RUN rm ~/.cache/matplotlib -rf

# install pcapplusplus
RUN wget https://github.com/seladb/PcapPlusPlus/releases/download/v21.05/pcapplusplus-21.05-ubuntu-20.04-gcc-9.tar.gz
RUN mkdir /pcapplusplus
RUN tar -C /pcapplusplus -xzvf pcapplusplus-21.05-ubuntu-20.04-gcc-9.tar.gz
WORKDIR pcapplusplus/pcapplusplus-21.05-ubuntu-20.04-gcc-9
RUN ./install.sh

# copy repos
RUN mkdir /emperor
COPY . /emperor

# install emperor deps
WORKDIR /emperor
RUN pip install --upgrade pip
RUN pip install -r requirements.txt




