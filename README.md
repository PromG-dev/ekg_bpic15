# Using Graph Databases for Event Data

## Installation
### PromG
The library can be installed in Pyhton using pip
`pip install promg`.

The source code for PromG can be found [PromG Core Github repository](https://github.com/PromG-dev/promg-core).

### Neo4j
The library assumes that Neo4j is installed.

Install [Neo4j](https://neo4j.com/download/):

- Use the [Neo4j Desktop](https://neo4j.com/download-center/#desktop)  (recommended), or
- [Neo4j Community Server](https://neo4j.com/download-center/#community)

## Get started

### Create a new graph database

- The scripts in this release assume password "12345678".
- The scripts assume the server to be available at the default URL `bolt://localhost:7687`
  - You can modify this also in the script.
- ensure to allocate enough memory to your database, advised: `dbms.memory.heap.max_size=5G`
- the script expects the `Neo4j APOC library` to be installed as a plugin, see https://neo4j.com/labs/apoc/

### Data set specific information
We provide data and scripts for

- BPIC14
- BPIC15
- BPIC16
- BPIC17
- BPIC19

For each of the datasets, we provide

- **data/.BPICXX/** - directory contains the original data in CSV format
  The datasets are available from:

            Esser, Stefan, & Fahland, Dirk. (2020). Event Data and Queries
            for Multi-Dimensional Event Data in the Neo4j Graph Database
            (Version 1.0) [Data set]. Zenodo. 
            http://doi.org/10.5281/zenodo.3865222
- **json_files/BPICXX.json** - json file that contains the semantic header for BPICXX
- **json_files/BPICXX_DS.json** - json file that contains a description for the different datasets for BPICXX (event
  tables etc)

For datasets BPIC14, BPIC16 we provide: 

- **file_preparation/bpicXX_prepare.py** - normalizes the original CSV data to an event table in CSV
  format required for the import and stores the output in the directory _ROOT/data/.BPICXX/prepared/_

For datasets BPIC15, BPIC17 and BPIC19 no preparation is required

### main script
There is one script that creates the Event/System knowledge graph: **main.py**

This script imports normalized event table of BPICXX from CSV files and executes several data modeling queries to construct
an event graph using the semantic header.

How to use
----------

For data import

1. start the Neo4j server
2. For BPIC14 and BPIC16, run bpicXX_prepare.py
3. set dataset_name to BPICXX in main.py and set use_sample to True/False
4. run main.py

