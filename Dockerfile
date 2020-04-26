FROM ubuntu:18.04
RUN apt-get update -y && \
    apt-get install -y python3-pip python-dev

# We copy just the requirements.txt first to leverage Docker cache
COPY requirements.txt /wecan/app/requirements.txt

WORKDIR /wecan/app

RUN pip3 install -r requirements.txt

COPY app /wecan/app/

WORKDIR /wecan/app/

RUN python3 wait_for_mysql.py
CMD gunicorn --bind 0.0.0.0:8000 flask_app:app
