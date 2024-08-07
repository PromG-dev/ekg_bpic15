# Event Knowledge Graph for BPIC15 Data
---------------------
## Installation
### Neo4j
The code assumes that Neo4j is installed.

Install [Neo4j](https://neo4j.com/download/):

- Use the [Neo4j Desktop](https://neo4j.com/download-center/#desktop)  (recommended), or
- [Neo4j Community Server](https://neo4j.com/download-center/#community)

### PromG
PromG should be installed as a Python package using pip
`pip install promg==2.0.0`.

The source code for PromG can be found [PromG Core Github repository](https://github.com/PromG-dev/promg-core).

---------------------
## Get started

### <a name="create_db"></a> Create a new graph database

- Create a New Graph Data In Neo4j Desktop
   1. Select `+Add` (Top right corner)
   2. Choose Local DBMS or Remote Connection
   3. Follow the prompted steps (the default password we assume is 12345678)
- Install APOC (see https://neo4j.com/labs/apoc/)
  - Install `Neo4j APOC Core library`: 
    1. Select the database in Neo4j desktop 
    2. On the right, click on the `plugins` tab > Open the `APOC` section > Click the `install` button
    3. Wait until a green check mark shows up next to `APOC` - that means it's good to go!
  - Install `Neo4j APOC Extended library`
    1. Download the [appropriate release](https://github.com/neo4j-contrib/neo4j-apoc-procedures/releases) (same version numbers as your Neo4j version)
       1. Look for the release that matches the version number of your Neo4j Database.
       2. Download the file `apoc-[your neo4j version]-extended.jar`
    2. Locate the `plugins` folder of your database:  
       Select the Neo4j Server in Neo4j Desktop > Click the three dots > Select `Open Folder` > Select `Plugins`
    4. Put `apoc-[your neo4j version]-extended.jar` into the `plugins` folder of your database
    5. Restart the server (database)
  - Configure extra settings using the configuration file `$NEO4J_HOME/conf/apoc.conf`
    1. Locate the `conf` folder of your database  
       Select the Neo4j Server in Neo4j Desktop > Click the three dots > Select `Open Folder` > Select `Conf`
    2. Create the file `apoc.conf`
    3. Add the following line to `apoc.conf`: `apoc.import.file.enabled=true`.
- Ensure to allocate enough memory to your database, advised: `dbms.memory.heap.max_size=10G`
  1. Select the Neo4j Server in Neo4j Desktop > Click the three dots > Select `Settings`
  2. Locate `dbms.memory.heap.max_size=512m`
  3. Change `512m` to `10G`
 
### Set configuration file
- Configuration; `config.yaml`
  - Set the URI in `config.yaml` to the URI of your server. Default value is `bolt://localhost:7687`.
  - Set the password in `config.yaml` to the password of your server. Default value is `12345678`.
  - Set the import directory in `config.yaml` to the import directory of your Neo4j server. You can determine the import directory as follows:
    1. Select the Neo4j Server in Neo4j Desktop > Click the three dots > Select `Open Folder` > Select `Import`
    2. This opens the import directory, so now you can copy the directory. 

### Store Data
We provide data and scripts for BPI Challenge 2015; store the original data in CSV format in the directory `/data`.
The datasets are available from:

            Esser, Stefan, & Fahland, Dirk. (2020). Event Data and Queries
            for Multi-Dimensional Event Data in the Neo4j Graph Database
            (Version 1.0) [Data set]. Zenodo. 
            http://doi.org/10.5281/zenodo.3865222

### Install PromG Library for Script
The library can be installed in Python using pip: `pip install promg==2.0.0`.
The source code for PromG can be found [PromG Core Github repository](https://github.com/PromG-dev/promg-core).

---------------------

## How to use
1. Set the configuration in `config.yaml`. 
   - For database settings, see [Create a new graph database](#create_db).
   - Set `use_sample` to True/False
2. start the Neo4j server
3. run main.py

------------------------

## Provided Scripts
### Main script
There is one script that creates the Event knowledge graph: **main.py**  
This script imports normalized event table of BPIC15 from CSV files and executes several data modeling queries to construct an event knowledge graph using the semantic header.

### Semantic header and dataset description in JSON files 
- **json_files/BPIC15.json** - json file that contains the semantic header for BPIC15
- **json_files/BPIC15_DS.json** - json file that contains a description for the different datasets for BPIC15 (event
  tables etc)



