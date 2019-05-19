Data Analytics/Processing Project

author: avinash.pasupulate@gmail.com

05/05/2019 00:03:54


**Status:**
In progress. . . .


**Generate Project Folder Structure:**
'''$sh project_structure_gen.sh'''


Using CMS dataset (2013) from kaggle

https://www.kaggle.com/cms/cms-open-payments-dataset-2013/downloads/cms-open-payments-dataset-2013.zip/2


**Terraform:**

* create separate terraform.tfvars for aws credentials locally

* using terraform to create an RDS instance to store raw data


'''$terraform apply -var-file="~/terraform.tfvars" -auto-approve'''

* Install terraform

* sudo conda install -y mysql-connector-python


* you ip http://checkip.amazonaws.com/

Create RDS:
'''sh pipeline/create_infra.sh'''

'''python3 src/preparation/data_ingestion.py'''


**Reference:**
* https://thuijskens.github.io/2018/11/13/useful-code-is-production-code/


**Setup:**
'''brew install mysql'''

**Docker_data_load:**
'''docker build --no-cache --rm -t avipasup/dataops_load_dev .'''
'''

Temporarily Created EC2 with role access to rds vpc and read s3
to deploy above docker container and load data to rds (resources would be destroyed once processed, so automating on requirement)
