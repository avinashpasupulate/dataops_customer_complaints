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
# TODO: write tests to run for individual files
# TODO: include logging and timing


@pytest.fixture
def load_fixture():
    """Import temp variable (test metrics) from a pickle file."""
    logging.info(" importing temp load test metrics from pickle file and testing")
    with open('test/tempdir/load_test_variable.dictionary', 'rb') as temp_var1:
        test_var = pickle.load(temp_var1)
    return test_var


@logger.timer
def test_load(load_fixture):
    """Run test variables for data load operation."""
    for i in load_fixture['db']:
        for j in load_fixture['files']:
            if i == j:
                # print(object['db'][i], object['db'][j])
                assert load_fixture['db'][i] == load_fixture['db'][j]
    logging.info(" completed load test to check number of rows")
