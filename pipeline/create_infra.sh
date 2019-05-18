# #!/usr/bin/env bash
TF_PATH=tf/dev
TF_CRED=~/terraform.tfvars
(cd $TF_PATH && terraform init)
(cd $TF_PATH && terraform apply -var-file=$TF_CRED -auto-approve)



#terraform apply -var-file=~/terraform.tfvars -auto-approve
