import os
import glob
import time
import pytest
import logging
import pandas as pd
import mysql.connector
from functools import wraps

class logger():

    def timer(func):
        """used for logging time"""

        @wraps(func)
        def wrapper(self, *args, **kwargs):
            t1 = time.time()
            resfunc = func(self, *args, **kwargs)
            t2 = time.time()-t1
            logging.info(' {} function was executed in {}'.format(func.__name__, t2))
            return resfunc

        return wrapper




class unitest(object):
    """checking if the length of columns are same"""
    # minor deviation is present

    def mysql_connection(**params):
        connection = mysql.connector.connect(**params)





    def return_len(self, file):
        df = pd.read_csv(file, usecols=[1]) # reading only 1st column temporarily
        return len(df)

    @logger.timer
    def setup(self):
        files = glob.glob('data/raw/*/*.csv')
        for file in files:
            dflen = self.return_len(file)
            print(dflen)

    def test():


    def teardown():
        return

if __name__ == "__main__":

    test = unitest()
    test.setup()
    #test.teardown()
