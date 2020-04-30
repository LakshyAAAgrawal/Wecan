# FROM ubuntu:18.04
# RUN apt-get update -y && \
#     apt-get install -y python3-pip python-dev

# COPY requirements.txt /app/requirements.txt
# RUN pip3 install -r /app/requirements.txt

# COPY . /app
# WORKDIR /app

# CMD python3 /app/main.py
FROM python:3.8.2-buster
COPY requirements.txt /app/requirements.txt
RUN pip3 install -r /app/requirements.txt
COPY . /app
WORKDIR /app
CMD python3 /app/main.py