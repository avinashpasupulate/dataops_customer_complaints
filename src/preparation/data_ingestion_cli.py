import os
import sys
import glob
import json
import yaml
#import getpass
import warnings
import subprocess
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
        with open(self.params['rds_attributes']['tf_path'], 'r') as f:
            tfstate = json.loads(f.read())
            self.attributes = tfstate['modules'][0]['resources']['aws_db_instance.default']['primary']['attributes']
            self.conninfo.extend((self.attributes['address'],
                                  self.attributes['name'],
                                  self.attributes['username'],
                                  self.attributes['password']))

    def bash_generator(self):
        # generates sql to load data to rds
        bash = []
        files = glob.glob('data/raw/*/*.csv')
        for raw_path in files:
            files = pd.read_csv(raw_path, sep = ',', error_bad_lines = False, dtype = object, nrows = 2)
            # table_name = os.path.basename(raw_path).split('.')[0] # filename used as table name
            bash_split = Template('''
                            cd {{data_path}}
                            split -b 100m {{source_file}} {{prefix}}.part_
                            mysqlimport --local --port=3306 -h {{host}} -u {{user}} -p{{pwd}} --fields-terminated-by=',' --fields-enclosed-by='"' --lines-terminated-by='\\n' {{dbname}} {{prefix}}.part_*
                            rm -r {{prefix}}.part_*
                        ''')
            parameters = {'data_path': os.path.dirname(os.path.abspath(raw_path)),
                          'source_file': os.path.basename(raw_path),
                          'prefix': os.path.basename(raw_path).split('.')[0],
                          'dbname': self.attributes['name'],
                          'host': self.attributes['address'],
                          'user': self.attributes['username'],
                          'pwd': self.attributes['password']
                         }
            bash.append(bash_split.render(**parameters))
        return ' '.join(i for i in bash)


    def sql_generator(self):
        # generates sql to load data to rds
        sql = []
        sql_drop = []
        files = glob.glob('data/raw/*/*.csv')
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
            ''')
            params = {'schema': self.conninfo[1],
                      'table_name': table_name,
                      'columns': cols
                     }

            drop_query = Template('''
                         -- drops first row containing header from table
                         delete from {{schema}}.{{table_name}} limit 1;
            ''')
            drop_params = {'schema': self.conninfo[1],
                           'table_name': table_name
                          }
            sql_drop.append(drop_query.render(**drop_params))
            sql.append(query.render(**params))
        return ['\n\n'.join(i for i in sql), '\n\n'.join(i for i in sql_drop)]

    def execute_query(self, query):
        try:
            # connecting to mysql rds instance
            connection = mysql.connector.connect(host = self.conninfo[0],
                                                 user = self.conninfo[2],
                                                 passwd = self.conninfo[3],
                                                 database = self.conninfo[1])
            print(connection)
            # executes query generated in the sql_generator function
            if connection.is_connected():
                dbinfo = connection.get_server_info()
                print('connected to mysql server version: {}'.format(dbinfo))
                cursor = connection.cursor()
                # setting max execution time to prevent timeouts when loading large files
                cursor.execute('set session max_execution_time=10800000;') # TODO:  self.params['rds_attributes']['execution_timeout'])
                # mysql connector cannot execute a sql script
                for command in query.split(';'):
                    try:
                        if len(command)>2:
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


    def execute_bash(self, bash):
        bash = '; '.join(i.strip() for i in bash.split('\n') if len(i.strip())>2)
        p = subprocess.Popen(bash, shell=True, stdout = subprocess.PIPE, bufsize=1)
        print(p.communicate()[0])
        print('bash: ', bash)

if __name__ == '__main__':
    parser = OptionParser(usage = "usage: python data_ingestion.py configfile sqloutput bashoutput", version = "1.0")
    opts, args = parser.parse_args()
    if len(args)<2:
        print('either config and/or output file is missing')
        exit(0)

    # importing parameters from config_prep.yaml file - uage of config.yaml is not required too few ext params, will be removed later on
    config = yaml.load(open(args[0], 'r'))
    generator = data_load(config)
    bash = generator.bash_generator()
    query = generator.sql_generator()

    # write sql statement to file
    with open(args[1], 'w') as f:
        f.write(bash)

    with open(args[2], 'w') as f:
        f.write(query[0])
    print('creating tables. . . . . \n')
    generator.execute_query(query[0])
    print('loading data to tables. . . . \n{}'.format(bash))
    generator.execute_bash(bash)
    print('dropping headers. . . .\n')
    generator.execute_query(query[1])
    print('completed. . . .')
