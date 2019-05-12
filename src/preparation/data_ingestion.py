import os
import glob
import json
import yaml
#import getpass
import warnings
import pandas as pd
import mysql.connector
from jinja2 import Template
from optparse import OptionParser

warnings.filterwarnings("ignore")

# TODO:  getting timeouts when loading large data - increased timeouts in rds tf
class data_load(object):
    def __init__(self, params):
        # initializing parameters
        self.params = params
        # getting rds details from tfstate file created after launch
        self.conninfo = []
        # TODO:  change relative path
        with open(cwd+self.params['rds_attributes']['tf_path'], 'r') as f:
            tfstate = json.loads(f.read())
            attributes = tfstate['modules'][0]['resources']['aws_db_instance.default']['primary']['attributes']
            self.conninfo.extend((attributes['address'],
                                  attributes['name'],
                                  attributes['username'],
                                  attributes['password']))

    def sql_generator(self):
        # generates sql to load data to rds
        sql = []
        files = glob.glob(cwd+'/data/raw/*/*.csv')
        for raw_path in files:
            files = pd.read_csv(raw_path, sep = ',', error_bad_lines = False, dtype = object, nrows = 10)
            # creating list of columns to include in ddl statement
            # TODO: currently using text data type, must be specific
            # truncate length of column names to less than 64 characters (max accepted by mysql)
            cols = ', \n\t\t\t\t\t'.join(i for i in [x.lower().replace(' ', '_')[0:62]+' text' for x in list(files.columns)])
            table_name = os.path.basename(raw_path).split('.')[0] # filename used as table name
            query = Template('''
                    -- parameterized script generated with python
                    -- create table to load {{table_name}} data
                    drop table if exists {{schema}}.{{table_name}};
                    create table if not exists {{schema}}.{{table_name}} (\t\t\t\t\t
                    {{columns}}
                     \t\t\t\t\t);
                    -- load raw csv data
                    load data local infile '{{raw_path}}'
                    into table {{schema}}.{{table_name}} fields terminated by ',' enclosed by '"' lines terminated by '\\r\\n' ignore 1 rows;
            ''')
            params = {'schema': self.params['database']['schema'],
                      'table_name': table_name,
                      'columns': cols,
                      'raw_path': raw_path
                     }
            sql.append(query.render(**params))
        return '\n\n'.join(i for i in sql)

    def execute_query(self, query):
        try:
            # connecting to mysql rds instance
            connection = mysql.connector.connect(host = self.conninfo[0],
                                                 user = self.conninfo[2],
                                                 passwd = self.conninfo[3],
                                                 database = self.conninfo[1])
            # executes query generated in the sql_generator function
            if connection.is_connected():
                dbinfo = connection.get_server_info()
                print('connected to mysql server version: {}'.format(dbinfo))
                cursor = connection.cursor()
                # mysql connector cannot execute a sql script
                for command in query.split(';'):
                    try:
                        if len(command)>1:
                            cursor.execute(command+';')
                            print(command)
                            print('############# completed ##################')
                    except IOError as msg:
                        print('error executing query. . {}'.format(msg))
        except mysql.connector.Error as e:
            print('error connecting to db: {} . . .'.format(e))
        finally:
            if connection.is_connected():
                cursor.close()
                connection.commit()
                connection.close()
                print('db connection is closed. . . ')

if __name__ == '__main__':
    cwd = os.getcwd()

    parser = OptionParser(usage = "usage: python data_ingestion.py configfile outputfile", version = "1.0")
    opts, args = parser.parse_args()
    if len(args)<2:
        print('include all (config/output) files')
        exit(0)

    # importing parameters from config_prep.yaml file
    config = yaml.load(open(args[0], 'r'))
    generator = data_load(config)
    query = generator.sql_generator()
    generator.execute_query(query)

    # write sql statement to file
    with open(args[1], 'w') as f:
        f.write(query)
