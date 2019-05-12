
import os
os.getcwd()

with open('/Users/Avinash/Documents/datascience/dataops/src/preparation/load_query_gen.sql', 'r') as f:
    q = f.read()

import mysql.connector
connection = mysql.connector.connect(host = 'terraform-20190512124433054400000001.csclevrtct8b.us-east-1.rds.amazonaws.com',
                                     user = 'opencmsuser',
                                     passwd = 'opencmspwd',
                                     database = 'opencmsdb')


cursor = connection.cursor()
cursor.execute(q)
