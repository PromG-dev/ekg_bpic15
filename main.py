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
from promg.modules.process_discovery import ProcessDiscovery

from custom_modules.custom_modules.df_interactions import InferDFInteractions
from custom_modules.custom_modules.delay_analysis import PerformanceAnalyzeDelays
from custom_modules.custom_modules.discover_dfg import DiscoverDFG

# several steps of import, each can be switch on/off
from colorama import Fore

connection = authentication.connections_map[authentication.Connections.LOCAL]

dataset_name = 'BPIC17'
use_sample = False
batch_size = 100000
use_preprocessed_files = False

semantic_header_path = Path(f'json_files/{dataset_name}.json')

semantic_header = SemanticHeader.create_semantic_header(semantic_header_path)
perf_path = os.path.join("..", "perf", dataset_name, f"{dataset_name}_{'sample_' * use_sample}Performance.csv")

ds_path = Path(f'json_files/{dataset_name}_DS.json')
dataset_descriptions = DatasetDescriptions(ds_path)

step_clear_db = False
step_populate_graph = False
step_infer_df_over_relations = False
step_discover_model = False
step_build_tasks = False
step_infer_delays = True

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

    if step_clear_db:
        print(Fore.RED + 'Clearing the database.' + Fore.RESET)
        db_manager.clear_db(replace=True)
        db_manager.set_constraints()

    if step_populate_graph:
        if use_preprocessed_files:
            print(Fore.RED + '💾 Preloaded files are used!' + Fore.RESET)
        else:
            print(Fore.RED + '📝 Importing and creating files' + Fore.RESET)

        oced_pg = OcedPg(dataset_descriptions=dataset_descriptions,
                         use_sample=use_sample,
                         use_preprocessed_files=use_preprocessed_files)
        oced_pg.run()
        oced_pg.create_df_edges()

    if step_infer_df_over_relations:
        print(Fore.RED + 'Inferring DF over relations between objects.' + Fore.RESET)
        infer_df_interactions = InferDFInteractions()
        infer_df_interactions.create_df_edges_for_relations('CASE_AO','DF_CASE_AO','CASE_AO')
        infer_df_interactions.delete_parallel_directly_follows_derived('DF_CASE_AO','DF_APPLICATION')
        infer_df_interactions.delete_parallel_directly_follows_derived('DF_CASE_AO','DF_OFFER')
        infer_df_interactions.create_df_edges_for_relations('CASE_AW','DF_CASE_AW','CASE_AW')
        infer_df_interactions.delete_parallel_directly_follows_derived('DF_CASE_AW','DF_APPLICATION')
        infer_df_interactions.delete_parallel_directly_follows_derived('DF_CASE_AW','DF_WORKFLOW')
        infer_df_interactions.create_df_edges_for_relations('CASE_WO','DF_CASE_WO','CASE_WO')
        infer_df_interactions.delete_parallel_directly_follows_derived('DF_CASE_WO','DF_WORKFLOW')
        infer_df_interactions.delete_parallel_directly_follows_derived('DF_CASE_WO','DF_OFFER')

    if step_discover_model:
        print(Fore.RED + 'Discovering multi-object DFG.' + Fore.RESET)
        dfg = DiscoverDFG()
        dfg.discover_dfg_for_entity("DF_APPLICATION","DF_A_APPLICATION",500,0.0)
        dfg.discover_dfg_for_entity("DF_OFFER","DF_A_OFFER",500,0.0)
        dfg.discover_dfg_for_entity("DF_WORKFLOW","DF_A_WORKFLOW",500,0.0)
        dfg.discover_dfg_for_entity("DF_CASE_AO","DF_A_CASE_AO",500,0.0)
        dfg.discover_dfg_for_entity("DF_CASE_AW","DF_A_CASE_AW",500,0.0)
        dfg.discover_dfg_for_entity("DF_CASE_WO","DF_A_CASE_WO",500,0.0)

    if step_build_tasks:
        print(Fore.RED + 'Detecting tasks.' + Fore.RESET)
        task_identifier = TaskIdentification(resource="Resource", case="CaseAWO")
        task_identifier.identify_tasks()
        task_identifier.aggregate_on_task_variant()

    if step_infer_delays:
        print(Fore.RED + 'Computing delay edges.' + Fore.RESET)
        delays = PerformanceAnalyzeDelays()
        #delays.enrich_with_delay_edges()
        #delays.analyze_delays()
        delays.visualize_delays(10000)

    performance.finish_and_save()
    db_manager.print_statistics()

    db_connection.close_connection()


if __name__ == "__main__":
    main()
