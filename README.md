# Using Graph Databases for Event Data

## Installation
### PromG
The library can be installed in Python using pip
`pip install promg==1.0.1`.

The source code for PromG can be found [PromG Core Github repository](https://github.com/PromG-dev/promg-core).

### Neo4j
The library assumes that Neo4j is installed.

Install [Neo4j](https://neo4j.com/download/):

- Use the [Neo4j Desktop](https://neo4j.com/download-center/#desktop)  (recommended), or
- [Neo4j Community Server](https://neo4j.com/download-center/#community)

## Get started

### Create a new graph database

- Configuration; `config.yaml`
  - Set the URI in `config.yaml` to the URI of your server. Default value is `bolt://localhost:7687`.
  - Set the password in `config.yaml` to the password of your server. Default value is `12345678`.
  - Set the import directory in `config.yaml` to the import directory of your Neo4j server (see https://neo4j.com/docs/operations-manual/current/configuration/file-locations/ under Import). 
- Ensure to allocate enough memory to your database, advised: `dbms.memory.heap.max_size=5G`
- Install APOC
  - The script expects the `Neo4j APOC Core library` AND `Neo4j APOC Extended library` to be installed as a plugin, see https://neo4j.com/labs/apoc/
  - Configure extra settings using the configuration file `$NEO4J_HOME/conf/apoc.conf`
    - In the conf file, you should add the following line `apoc.import.file.enabled=true`.

## Data set specific information
We provide data and scripts for BPI Challenge 2015; store the original data in CSV format in the directory `/data`.
The datasets are available from:

            Esser, Stefan, & Fahland, Dirk. (2020). Event Data and Queries
            for Multi-Dimensional Event Data in the Neo4j Graph Database
            (Version 1.0) [Data set]. Zenodo. 
            http://doi.org/10.5281/zenodo.3865222

## JSON 
- **json_files/BPIC15.json** - json file that contains the semantic header for BPIC15
- **json_files/BPIC15_DS.json** - json file that contains a description for the different datasets for BPIC15 (event
  tables etc)

### main script
There is one script that creates the Event knowledge graph: **main.py**

This script imports normalized event table of BPIC15 from CSV files and executes several data modeling queries to construct an event knowledge graph using the semantic header.

How to use
----------

For data import

1. Set the configuration in `config.yaml`. 
   - For database settings, see [Create a new graph database](### Create a new graph database).
   - Set `use_sample` to True/False
2. start the Neo4j server
3. run main.py


