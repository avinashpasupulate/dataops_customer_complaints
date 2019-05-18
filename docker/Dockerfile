FROM continuumio/miniconda3

RUN  apt-get update -y && \
     apt-get upgrade -y && \
     apt-get dist-upgrade -y && \
     apt-get -y autoremove && \
     apt-get clean && \
     apt-get install -y --no-install-recommends apt-utils dialog unzip nano && \
     conda install pip -y && \
     pip install awscli --upgrade && \
     mkdir .aws

COPY . /

RUN apt-get update -y && \
    git clone -b beta https://github.com/avinashpasupulate/dataops_opencms_data.git && \
    unzip terraform_0.11.14_linux_amd64.zip && \
    mv terraform /usr/local/bin && \
    rm -r terraform_0.11.14_linux_amd64.zip

WORKDIR /dataops_opencms_data
