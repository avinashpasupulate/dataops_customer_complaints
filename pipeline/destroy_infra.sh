# #!/usr/bin/env bash
TF_PATH=tf/dev/load
(cd $TF_PATH && terraform destroy -auto-approve)
