FROM continuumio/miniconda3:4.12.0

RUN apt update \
    && apt -y upgrade \
    && apt -y install postgresql-client

WORKDIR /gearmap

ADD devops ./devops
ADD common ./common
ADD src ./src

RUN mkdir ./logs
RUN conda env create -f ./devops/conda_env.yml
RUN conda clean -afy

EXPOSE 5001

ENTRYPOINT ["bash", "+x", "./devops/src/docker/entrypoint.sh"]