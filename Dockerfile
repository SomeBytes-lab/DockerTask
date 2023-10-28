FROM ubuntu:latest 

RUN apt-get update && apt-get -y install python3 python3-pip
RUN python3 -m pip install beautifulsoup4 bottle requests textblob
RUN python3 -m textblob.download_corpora

COPY main.py wordparser.py
