FROM python:3.8.12

# just in case
ENV DEBIAN_FRONTEND=noninteractive
SHELL ["/bin/bash", "-c"]

# deps
RUN apt update && apt install -y graphviz fonts-roboto
RUN rm ~/.cache/matplotlib -rf

# copy repos
RUN mkdir /emperor
COPY . /emperor

# install emperor deps
WORKDIR /emperor
RUN pip install --upgrade pip
RUN pip install -r requirements.txt
