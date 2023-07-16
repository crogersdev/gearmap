FROM python:3.9-slim-buster

RUN apt update \
    && apt -y upgrade \
    && apt -y install postgresql-client \
    && apt -y install python3-dev libpq-dev \
    && apt -y install build-essential

WORKDIR /gearmap

COPY . .

RUN mkdir ./logs
# necessary for anyjson as of 19 june 2023
RUN pip install "setuptools<58.0.0"
RUN pip install -r /gearmap/devops/requirements.txt

# EXPOSE 5001

# ENTRYPOINT ["bash", "+x", "./devops/src/docker/entrypoint.sh"]
