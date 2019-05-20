FROM continuumio/miniconda3

RUN  apt-get update -y && \
     apt-get upgrade -y && \
     apt-get dist-upgrade -y && \
     apt-get -y autoremove && \
     apt-get clean && \
     apt-get install -y --no-install-recommends apt-utils dialog unzip nano

RUN apt-get update -y && \
    git clone -b beta https://github.com/avinashpasupulate/dataops_opencms_data.git && \
    wget https://releases.hashicorp.com/terraform/0.11.14/terraform_0.11.14_linux_amd64.zip && \
    unzip terraform_0.11.14_linux_amd64.zip && \
    mv terraform /usr/local/bin && \
    rm -r terraform_0.11.14_linux_amd64.zip && \
    apt-get install -y mysql-client

WORKDIR dataops_opencms_data

ENTRYPOINT conda install -y pip \
                            pandas==0.23.4 \
                            mysql==5.7.22 \
                            jinja2==2.10 \
                            yaml==0.1.7 && \
           pip install awscli --upgrade \
                       mysql-connector-python && \
           aws s3 cp s3://dataops-opencms/pgyr17_p011819.zip /dataops_opencms_data/data/raw/ && \
           unzip /dataops_opencms_data/data/raw/pgyr17_p011819.zip && \
           sh pipeline/create_infra.sh && \
           aws s3 cp /dataops_opencms_data/tf/dev/terraform.tfstate s3://dataops-opencms/terraform.tfstate && \
           sh pipeline/data_ingestion.sh
