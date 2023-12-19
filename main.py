from datetime import datetime

from promg import SemanticHeader, OcedPg
from promg import DatabaseConnection
from promg import DatasetDescriptions
from promg import Configuration

from promg import Performance
from promg.modules.db_management import DBManagement
from promg.modules.task_identification import TaskIdentification

from custom_modules.custom_modules.df_interactions import InferDFInteractions
from custom_modules.custom_modules.delay_analysis import PerformanceAnalyzeDelays
from custom_modules.custom_modules.discover_dfg import DiscoverDFG


from colorama import Fore

config = Configuration()
semantic_header = SemanticHeader.create_semantic_header(config=config)
dataset_descriptions = DatasetDescriptions(config=config)

# several steps of import, each can be switch on/off
step_clear_db = True
step_populate_graph = True
step_delete_parallel_df = True
step_discover_model = True
step_build_tasks = True
step_infer_delays = True


def main() -> None:
    """
    Main function, read all the logs, clear and create the graph, perform checks
    @return: None
    """
    print("Started at =", datetime.now().strftime("%H:%M:%S"))

    db_connection = DatabaseConnection.set_up_connection_using_config(config=config)
    performance = Performance.set_up_performance(config=config)
    db_manager = DBManagement()

    if step_clear_db:
        print(Fore.RED + 'Clearing the database.' + Fore.RESET)
        db_manager.clear_db(replace=True)
        db_manager.set_constraints()

    if step_populate_graph:
        if config.use_preprocessed_files:
            print(Fore.RED + '💾 Preloaded files are used!' + Fore.RESET)
        else:
            print(Fore.RED + '📝 Importing and creating files' + Fore.RESET)

        oced_pg = OcedPg(dataset_descriptions=dataset_descriptions,
                         use_sample=config.use_sample,
                         use_preprocessed_files=config.use_preprocessed_files)
        # import_directory=config.import_directory)
        oced_pg.load_and_transform()
        oced_pg.create_df_edges()

    if config.db_name == 'BPIC17':
        if step_delete_parallel_df:
            print(Fore.RED + 'Inferring DF over relations between objects.' + Fore.RESET)
            infer_df_interactions = InferDFInteractions()
            infer_df_interactions.delete_parallel_directly_follows_derived('CASE_AO', 'Application')
            infer_df_interactions.delete_parallel_directly_follows_derived('CASE_AO', 'Offer')
            infer_df_interactions.delete_parallel_directly_follows_derived('CASE_AW', 'Application')
            infer_df_interactions.delete_parallel_directly_follows_derived('CASE_AW', 'Workflow')
            infer_df_interactions.delete_parallel_directly_follows_derived('CASE_WO', 'Workflow')
            infer_df_interactions.delete_parallel_directly_follows_derived('CASE_WO', 'Offer')

        if step_discover_model:
            print(Fore.RED + 'Discovering multi-object DFG.' + Fore.RESET)
            dfg = DiscoverDFG()
            dfg.discover_dfg_for_entity("Application", 25000, 0.0)
            dfg.discover_dfg_for_entity("Offer", 25000, 0.0)
            dfg.discover_dfg_for_entity("Workflow", 25000, 0.0)
            dfg.discover_dfg_for_entity("CASE_AO", 25000, 0.0)
            dfg.discover_dfg_for_entity("CASE_AW", 25000, 0.0)
            dfg.discover_dfg_for_entity("CASE_WO", 25000, 0.0)

        if step_build_tasks:
            print(Fore.RED + 'Detecting tasks.' + Fore.RESET)
            task_identifier = TaskIdentification(resource="Resource", case="CaseAWO")
            task_identifier.identify_tasks()
            task_identifier.aggregate_on_task_variant()

        if step_infer_delays:
            print(Fore.RED + 'Computing delay edges.' + Fore.RESET)
            delays = PerformanceAnalyzeDelays()
            # delays.enrich_with_delay_edges()
            # delays.analyze_delays()
            delays.visualize_delays(10000)

    performance.finish_and_save()
    db_manager.print_statistics()

    db_connection.close_connection()


if __name__ == "__main__":
    main()
