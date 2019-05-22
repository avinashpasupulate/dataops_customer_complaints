#!bin/bash

#commands
sudo -s
yum update -y
amazon-linux-extras install docker -y
service docker start
usermod -a -G docker ec2-user
docker pull avipasup/dataops_load_dev:latest
docker run --rm -it avipasup/dataops_load_dev:latest /bin/bash
