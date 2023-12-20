from datetime import datetime

from promg import SemanticHeader, OcedPg
from promg import DatabaseConnection
from promg import DatasetDescriptions
from promg import Configuration

from promg import Performance
from promg.modules.db_management import DBManagement

from colorama import Fore

config = Configuration()
semantic_header = SemanticHeader.create_semantic_header(config=config)
dataset_descriptions = DatasetDescriptions(config=config)

# several steps of import, each can be switch on/off
step_clear_db = True
step_populate_graph = True


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

    performance.finish_and_save()
    db_manager.print_statistics()

    db_connection.close_connection()


if __name__ == "__main__":
    main()
