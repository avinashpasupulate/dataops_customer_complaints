provider "aws" {
    region = "us-east-1"
    shared_credentials_file = "/Users/avinashpasupulate/.aws/credentials"
    profile = "default"
}

#resource "aws_instance" "model" {
#    ami = "ami-2757f631"
#    instance_type = "t2.micro"
#}

#vpc
resource "aws_default_vpc" "default" {
}

#data - changed to private ip
data "http" "ip" {
    url = "http://ipv4.icanhazip.com"
}
#url = "http://169.254.169.254/latest/meta-data/local-ipv4/"


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
        cidr_blocks = ["${chomp(data.http.ip.body)}/32"]
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

resource "aws_db_parameter_group" "default" {
        name = "rds-pg"
        family = "mysql5.7"

        parameter {
                  name = "max_execution_time"
                  value = 10800000
        }

        parameter {
                  name = "sql_mode"
                  value = "NO_ENGINE_SUBSTITUTION"
        }

        parameter {
                  name = "max_allowed_packet"
                  value = 512000000
        }

        parameter {
                  name = "net_write_timeout"
                  value = 10800000
        }

        parameter {
                  name = "net_read_timeout"
                  value = 10800000
        }

        parameter {
                  name = "connect_timeout"
                  value = 10800000
        }

        parameter {
                  name = "wait_timeout"
                  value = 10800000
        }

        parameter {
                  name = "interactive_timeout"
                  value = 10800000
        }

        parameter {
                  name = "bulk_insert_buffer_size"
                  value = 512000000
        }
}

resource "aws_db_instance" "default" {
    allocated_storage = 20
    storage_type = "gp2"
    instance_class = "db.t2.micro"
    publicly_accessible = true
    skip_final_snapshot = true
    backup_retention_period = 0
    engine = "mysql"
    name = "opencmsdb"
    parameter_group_name = "${aws_db_parameter_group.default.id}"
    username = "${random_string.uname.result}"
    password = "${random_string.key.result}"
    vpc_security_group_ids = ["${aws_default_security_group.default.id}"]

    timeouts {
        create = "3h",
        delete = "3h",
        update = "3h"
        }
}
