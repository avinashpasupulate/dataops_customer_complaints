#!/bin/bash
sudo -s
curl -fsSL https://download.docker.com/linux/ubuntu/gpg | apt-key add -
add-apt-repository "deb [arch=amd64] https://download.docker.com/linux/ubuntu $(lsb_release -cs) stable"
apt-get update -y
apt-cache policy docker-ce
apt-get install -y docker-ce
service docker start
usermod -a -G docker ubuntu
docker pull avipasup/dataops_load_dev:latest
docker run --rm -it avipasup/dataops_load_dev:latest /bin/bash
