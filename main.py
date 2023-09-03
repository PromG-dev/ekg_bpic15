import os
from datetime import datetime
from pathlib import Path

from promg import SemanticHeader, OcedPg
from promg import DatabaseConnection
from promg import authentication
from promg import DatasetDescriptions

from promg import Performance
from promg.modules.db_management import DBManagement
from promg.modules.task_identification import TaskIdentification

from ekg_creator_custom.ekg_modules.ekg_custom_module import CustomModule

# several steps of import, each can be switch on/off
from colorama import Fore

connection = authentication.connections_map[authentication.Connections.LOCAL]

dataset_name = 'BPIC17'
use_sample = True
batch_size = 10000
use_preprocessed_files = False

semantic_header_path = Path(f'json_files/{dataset_name}.json')

semantic_header = SemanticHeader.create_semantic_header(semantic_header_path)
perf_path = os.path.join("..", "perf", dataset_name, f"{dataset_name}_{'sample_' * use_sample}Performance.csv")

ds_path = Path(f'json_files/{dataset_name}_DS.json')
dataset_descriptions = DatasetDescriptions(ds_path)

step_clear_db = True
step_populate_graph = True
step_build_tasks = True

verbose = False
credentials_key = authentication.Connections.LOCAL


def main() -> None:
    """
    Main function, read all the logs, clear and create the graph, perform checks
    @return: None
    """
    print("Started at =", datetime.now().strftime("%H:%M:%S"))

    db_connection = DatabaseConnection.set_up_connection_using_key(key=credentials_key,
                                                                   verbose=verbose)
    performance = Performance.set_up_performance(dataset_name=dataset_name,
                                                 use_sample=use_sample)
    db_manager = DBManagement()

    if use_preprocessed_files:
        print(Fore.RED + '💾 Preloaded files are used!' + Fore.RESET)
    else:
        print(Fore.RED + '📝 Importing and creating files' + Fore.RESET)

    if step_clear_db:
        db_manager.clear_db(replace=True)
        db_manager.set_constraints()

    if step_populate_graph:
        oced_pg = OcedPg(dataset_descriptions=dataset_descriptions,
                         use_sample=use_sample,
                         use_preprocessed_files=use_preprocessed_files)
        oced_pg.run()
        oced_pg.create_df_edges()

    if step_build_tasks:
        task_identifier = TaskIdentification(resource="Resource", case="CaseAWO")
        task_identifier.identify_tasks()
        task_identifier.aggregate_on_task_variant()

    performance.finish_and_save()
    db_manager.print_statistics()

    db_connection.close_connection()


if __name__ == "__main__":
    main()
