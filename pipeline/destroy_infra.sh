# #!/usr/bin/env bash
TF_PATH=tf/dev
(cd $TF_PATH && terraform destroy -auto-approve)
