import mysql.connector
import json
import os

cwd = os.getcwd()
with open(cwd+'/tf/dev/terraform.tfstate', 'r') as f:
    tfstate = json.loads(f.read())
    attributes = tfstate['modules'][0]['resources']['aws_db_instance.default']['primary']['attributes']
    address = attributes['address']
    db_name = attributes['name']
    uname = attributes['username']
    password = attributes['password']

connection = mysql.connector.connect(host = address,
                                     user = uname,
                                     passwd = password,
                                     database = db_name)
