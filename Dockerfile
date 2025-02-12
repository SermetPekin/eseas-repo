FROM ubuntu:20.04
RUN apt-get update && apt-get install -y python3.9 python3.9-dev
COPY . .

RUN pip install --no-cache-dir -r ./requirements.txt


FROM openjdk:11
COPY . /usr/src/app

WORKDIR /usr/src/app

COPY requirements.txt ./

# Java jwsacruncher
RUN wget https://github.com/jdemetra/jwsacruncher/releases/download/v2.2.4/jwsacruncher-2.2.4-bin.zip && \
    unzip jwsacruncher-2.2.4-bin.zip -d /usr/src/app/ && \
    rm jwsacruncher-2.2.4-bin.zip

ENV PYTHONUNBUFFERED=1
# python
RUN apt-get update && apt-get install -y python3.9 python3.9-dev  python3-pip
RUN python3 -m pip install --no-cache-dir -r ./requirements.txt

# Tests
RUN python3 -m pip install pytest
ENV PYTHONUNBUFFERED=1
ENV JAVA_CRUNCHER_BIN='/usr/src/app/jwsacruncher-2.2.4/bin'
RUN mkdir test_out
RUN python3 ./main2.py

# docker build -t eseas .
# docker run --rm eseas
