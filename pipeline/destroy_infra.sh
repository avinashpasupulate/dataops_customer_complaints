# #!/usr/bin/env bash
TF_PATH=tf/dev
TF_CRED=~/terraform.tfvars
(cd $TF_PATH && terraform destroy -var-file=$TF_CRED -auto-approve)
