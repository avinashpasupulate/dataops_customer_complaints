provider "aws" {
    region = "us-east-1"
    shared_credentials_file = "/Users/avinashpasupulate/.aws/credentials"
    profile = "default"
}

resource "aws_default_security_group" "default" {
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
