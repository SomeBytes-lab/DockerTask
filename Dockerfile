FROM ubuntu:latest 

RUN apt-get update && apt-get -y install python3 python3-pip
RUN python3 -m pip install beautifulsoup4 bottle requests textblob
RUN python3 -m textblob.download_corpora

EXPOSE 8080
EXPOSE 8081
EXPOSE 8082

COPY main.py wordparser.py
