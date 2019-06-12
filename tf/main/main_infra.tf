provider "aws"{
          region = "us-east-1"
          shared_credentials_file = "Users/avinashpasupulate/.aws/credentials"
          profile = "default"
}


#vpc
resource "aws_default_vpc" "default" {
}

#data
data "http" "ip" {
      url = "http://ipv4.icanhazip.com"
}

#url = "http://169.254.169.254/latest/meta-data/local-ipv4/"


#modifying already existing default vpc and subnet groups
#subnet
resource "aws_default_subnet" "default" {
          availability_zone = "us-east-1a"
}

#security group
resource "aws_default_security_group" "default" {
          vpc_id = "${aws_default_vpc.default.id}"

          # inbound traffic only on 3306 from instance
          ingress{
                  from_port = "3306"
                  to_port = "3306"
                  protocol = "tcp"
                  cidr_blocks = ["172.31.48.100/32"]
                  }

          #temporarily allowing inbound traffic to rds for querying
          ingress{
                  from_port = "3306"
                  to_port = "3306"
                  protocol = "tcp"
                  cidr_blocks = ["0.0.0.0/0"]
                  }

          #allowing all outbound traffic
          egress{
                  from_port = 0
                  to_port = 0
                  protocol = "-1"
                  cidr_blocks = ["0.0.0.0/0"]
                  }
}

data "template_file" "userdata" {
      template = "${file("${path.cwd}/bootstrap_main.sh")}"
}


data "aws_ami" "ubuntu" {
      most_recent = true
      filter {
              name   = "name"
              values = ["ubuntu/images/hvm-ssd/ubuntu-xenial-16.04-amd64-server-*"]
              }
      filter {
              name   = "virtualization-type"
              values = ["hvm"]
              }
      owners = ["099720109477"] # Canonical
}

resource "aws_instance" "main_test" {
          ami = "${data.aws_ami.ubuntu.id}"
          instance_type = "t2.micro"
          security_groups = ["${aws_default_security_group.default.id}"]
          subnet_id = "${aws_default_subnet.default.id}"
          iam_instance_profile = "s3_ec2_vpc_admin"
          private_ip = "172.31.48.100"
          user_data = "${data.template_file.userdata.template}"
}
