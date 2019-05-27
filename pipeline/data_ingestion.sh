#!/usr/bin/env bash
DATA_ING=src/preparation
mkdir $DATA_ING/output_load
python3 $DATA_ING/data_ingestion_cli.py $DATA_ING/config_prep.yaml $DATA_ING/output_load/load_bash_gen.sh $DATA_ING/output_load/create_load_query_gen.sql
