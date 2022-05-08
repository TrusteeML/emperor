FROM ubuntu:19.10

# just in case
ENV DEBIAN_FRONTEND=noninteractive
SHELL ["/bin/bash", "-c"]

# fix apt sources
RUN sed -i -e 's/archive.ubuntu.com\|security.ubuntu.com/old-releases.ubuntu.com/g' /etc/apt/sources.list

# deps
RUN apt update && apt install -y libpcap-dev python3-dev python3-pip wget make build-essential libssl-dev zlib1g-dev \
  libbz2-dev libreadline-dev libsqlite3-dev wget curl llvm curl git \
  libncursesw5-dev xz-utils tk-dev libxml2-dev libxmlsec1-dev libffi-dev liblzma-dev \ 
  graphviz fonts-roboto msttcorefonts
RUN rm ~/.cache/matplotlib -rf


# install poetry
RUN pip3 install --upgrade pip
RUN pip3 install poetry

# copy repos
RUN mkdir /emperor
COPY . /emperor

# install emperor deps
WORKDIR /emperor
# these deps were throwing an error
RUN pip3 install --ignore-installed PyYAML entrypoints 
RUN poetry config virtualenvs.create false && poetry install
