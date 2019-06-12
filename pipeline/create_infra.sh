# #!/usr/bin/env bash
TF_PATH=tf/dev/load
(cd $TF_PATH && terraform init)
(cd $TF_PATH && terraform apply -auto-approve)



#terraform apply -var-file=~/terraform.tfvars -auto-approve
