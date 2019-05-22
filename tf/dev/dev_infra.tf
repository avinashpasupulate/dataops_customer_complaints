provider "aws" {
    region = "us-east-1"
    profile = "default"
}

#resource "aws_instance" "model" {
#    ami = "ami-2757f631"
#    instance_type = "t2.micro"
#}

#vpc
resource "aws_default_vpc" "default" {
}

#data
data "http" "ip" {
    url = "http://ipv4.icanhazip.com"
}

#subnet
resource "aws_default_subnet" "default" {
    availability_zone = "us-east-1a"
}

#security group
resource "aws_default_security_group" "default" {
    vpc_id = "${aws_default_vpc.default.id}"
    #all inbound traffic only on 3306
    ingress{
        from_port = "3306"
        to_port = "3306"
        protocol = "tcp"
        cidr_blocks = ["${chomp(data.http.ip.body)}/32"]
    }
    #allowing all outbound traffic
    egress{
        from_port = 0
        to_port = 0
        protocol = "-1"
        cidr_blocks = ["0.0.0.0/0"]
    }
}

resource "random_string" "uname" {
    length = 10
    special = false
    number = false
    upper = false
}

resource "random_string" "key" {
    length = 10
    special = false
    number = true
}

resource "aws_db_instance" "default" {
    allocated_storage = 20
    storage_type = "gp2"
    instance_class = "db.t2.micro"
    publicly_accessible = true
    skip_final_snapshot = true
    engine = "mysql"
    name = "opencmsdb"
    username = "${random_string.uname.result}"
    password = "${random_string.key.result}"
    vpc_security_group_ids = ["${aws_default_security_group.default.id}"]

    timeouts {
        create = "3h",
        delete = "3h",
        update = "3h"
        }
}
