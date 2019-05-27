import os
import sys
import glob
import json
import yaml
import signal
#import getpass
import warnings
import subprocess
import pandas as pd
import mysql.connector
from jinja2 import Template
from optparse import OptionParser

warnings.filterwarnings("ignore")

class data_load(object):
    def __init__(self, params):
        # initializing parameters
        self.params = params
        # getting rds details from tfstate file created after launch
        self.conninfo = []
        self.rollback = 'sh pipeline/destroy_infra.sh'
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
            bash_split = Template('''
                            cd {{data_path}}
                            echo "loading to {{prefix}} table . . . "
                            split -a 6 -b 15m {{source_file}} {{prefix}}.part_
                            mysqlimport --local --use-threads 4 --compress --port=3306 -h {{host}} -u {{user}} -p{{pwd}} --fields-terminated-by=',' --fields-enclosed-by='"' --lines-terminated-by='\\n' {{dbname}} {{prefix}}.part_*
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
            # executes query generated in the sql_generator function
            if connection.is_connected():
                dbinfo = connection.get_server_info()
                print('\nconnected to mysql server version: {}'.format(dbinfo))
                cursor = connection.cursor()
                # setting max execution time, max_packet_size to prevent timeouts when loading large files

                # mysql connector cannot execute a sql script
                for command in query.split(';'):
                    try:
                        if len(command.strip())>2:
                            cursor.execute(command+';')
                            print(command)
                            print('\n############# completed ##################\n')
                    except IOError as msg:
                        print('\nerror executing query. . {}\n'.format(msg))
                        print('\nrolling back deployed resources . . . \n')
                        #generator.execute_bash(self.rollback)
                        exit(0)
        except mysql.connector.Error as e:
            print('\nerror connecting to db: {} . . .'.format(e))
            print('\nrolling back deployed resources . . . \n')
            #generator.execute_bash(self.rollback)
            exit(0)
        finally:
            if connection.is_connected():
                cursor.close()
                connection.commit()
                connection.close()
                print('\ndb connection is closed. . . \n')

    def execute_bash(self, bash):
        bash = '; '.join(i.strip() for i in bash.split('\n') if len(i.strip())>2)
        p = subprocess.Popen(bash, shell=True, stdout = subprocess.PIPE, bufsize=1, preexec_fn=os.setsid)
        for i in iter(p.stdout.readline, ''):
            if i != b'':
                print(i.decode('UTF-8'))
        p.stdout.close()

if __name__ == '__main__':
    # TODO: include more error handlers, rollback & unit tests (pyunit)
    # TODO: Integrate with jenkins
    parser = OptionParser(usage = "usage: python data_ingestion.py configfile sqloutput bashoutput", version = "1.0")
    opts, args = parser.parse_args()
    if len(args)<2:
        print('\neither config and/or output file is missing . . .\n')
        exit(0)

    # importing parameters from config_prep.yaml file - uage of config.yaml is not required too few ext params, will be removed later on
    config = yaml.load(open(args[0], 'r'))
    try:
        generator = data_load(config)
    except:
        print('\none of the configuration parameters is not defined properly, most likely .tfstate is not populated yet. . . \n')
        exit(0)
    bash = generator.bash_generator()
    query = generator.sql_generator()

    # write sql statement to file
    with open(args[1], 'w') as f:
        f.write(bash)

    with open(args[2], 'w') as f:
        f.write(query[0])
    print('\ncreating tables. . . . . \n')
    generator.execute_query(query[0])
    print('\nloading data to tables. . . . \n')
    generator.execute_bash(bash)
    print('\ndropping headers. . . .\n')
    generator.execute_query(query[1])
    print('\ncompleted. . . .\n')
