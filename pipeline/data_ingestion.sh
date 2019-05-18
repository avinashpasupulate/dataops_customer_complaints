#!/usr/bin/env bash
DATA_ING=/src/preparation
python3 $DATA_ING/data_ingestion.py $DATA_ING/config_prep.yaml $DATA_ING/load_query_gen.sql
