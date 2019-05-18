#!/usr/bin/env bash
DATA_ING=src/preparation
python3 $DATA_ING/data_ingestion_cli.py $DATA_ING/config_prep.yaml $DATA_ING/create_query_gen.sql $DATA_ING/load_bash_gen.sh
