Data Analytics/Processing Project
author: avinash.pasupulate@gmail.com
05/05/2019 00:03:54

**Status:**
In progress. . . .

**Generate Project Folder Structure:**
'''$sh project_structure_gen.sh'''

Using consumer complaints dataset from
https://www.consumerfinance.gov/data-research/consumer-complaints/

Consumer Complaint Database


**Terraform:**
* create separate terraform.tfvars for aws credentials locally
* using terraform to create an RDS instance to store raw data

'''$terraform apply -var-file="~/terraform.tfvars" -auto-approve'''

* Install terraform
* sudo conda install -y mysql-connector-python


* you ip http://checkip.amazonaws.com/
