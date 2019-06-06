#!/usr/bin/env bash
# generating data science project folder structure
#avinash.pasupulate@gmail.com

mkdir -p src             # storing source code used during stages of project
mkdir -p src/preparation # data ingestion
mkdir -p src/processing  # data processing
mkdir -p src/modelling   # modelling

mkdir -p test            # unit tests for code
mkdir -p test/tempdir    # temp dir to store intermediate object files
mkdir -p model           # storing intermediate results

mkdir -p data            # storing project relevant data
mkdir -p data/raw        # storing raw data
mkdir -p data/processed  # storing processed data

mkdir -p notebook        # notebooks for interactive and presentable code
mkdir -p notebook/eda    # eda notebooks
mkdir -p notebook/poc    # poc notebooks
mkdir -p notebook/modelling # modelling notebooks
mkdir -p notebook/evaluation # model evaluation notebook

mkdir -p pipeline        # model automation pipeline

mkdir -p tf              # generating infra for running model
mkdir -p tf/dev          # terraform files for dev environment
mkdir -p tf/preprod      # terraform files for staging environment
mkdir -p tf/prod         # terraform files for production environment

mkdir -p docs            # storing documentation product requirement & technical design specs, etc

# creating readme
echo "Data Analytics/Processing Project \n\nauthor: avinash.pasupulate@gmail.com" >> Readme.md
date +"%d/%m/%Y %T" >> Readme.md
echo "\n\nGenerate Project Folder Structure: \nsh project_structure_gen.sh" >> Readme.md
