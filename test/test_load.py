"""
Test outputs from the prep scripts.

avinash.pasupulate@gmail.com
"""

import sys
import pickle
import pytest
import logging
from functools import wraps

sys.path.append('src/preparation/')

from data_ingestion_cli import logger

logging.info(" importing temp load test metrics from pickle file and testing")
with open('test/tempdir/load_test_variable.dictionary', 'rb') as temp_var1:
    test_var = pickle.load(temp_var1)

table_name = []
vals = []
for i, j in zip(test_var['db'], test_var['files']):
    if i == j:
        table_name.append(i)
        val_l = [test_var['db'][i]]
        val_l.append(test_var['files'][j])
        vals.append(tuple(val_l))


@logger.timer
@pytest.mark.parametrize("t_input, expected", vals, ids=table_name)
def test_load(t_input, expected):
    """
    Run test variables for data load operation.

    passes test if there is less than 500 rows difference.
    due to variation caused when parsing csv (to be corrected)
    """
    assert abs(t_input-expected) < 500
    logging.info(" completed load test to check number of rows")
