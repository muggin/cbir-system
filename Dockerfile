FROM ubuntu:16.04

RUN apt-get update && apt-get install python python-pip iputils-ping -y
RUN pip install flask
RUN pip install flask_cors

ADD requirements.txt requirements.txt

RUN pip install -r requirements.txt

ADD . /app
WORKDIR /app
