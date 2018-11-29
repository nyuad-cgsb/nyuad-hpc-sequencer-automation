FROM continuumio/miniconda3:4.5.11

RUN apt-get update -y; apt-get upgrade -y
RUN apt-get install -y vim-tiny vim-athena mysql-client ssh

RUN adduser --home /home/airflow airflow

USER airflow
WORKDIR /home/airflow

COPY environment.yml environment.yml

RUN conda env create -f environment.yml
RUN echo "alias l='ls -lah'" >> ~/.bashrc
RUN echo "source activate sequencer-automation" >> ~/.bashrc

ENV CONDA_EXE /opt/conda/bin/conda
ENV CONDA_PREFIX /home/airflow/.conda/envs/sequencer-automation
ENV CONDA_PYTHON_EXE /opt/conda/bin/python
ENV CONDA_PROMPT_MODIFIER (sequencer-automation)
ENV CONDA_DEFAULT_ENV sequencer-automation
ENV PATH /home/airflow/.conda/envs/sequencer-automation/bin:/opt/conda/bin:/usr/local/sbin:/usr/local/bin:/usr/sbin:/usr/bin:/sbin:/bin

COPY airflow/airflow.cfg /home/airflow/airflow/airflow.cfg
#CMD airflow initdb
