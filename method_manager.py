from colorama import Fore

from module_manager import ModuleManager


class MethodManager:
    def __init__(self, config=None):
        self.modules = ModuleManager(config=config)

    def clear_database(self):
        db_manager = self.modules.get_db_manager()
        print(Fore.RED + 'Clearing the database.' + Fore.RESET)
        db_manager.clear_db(replace=True)
        db_manager.set_constraints()

    def load_and_transform_records(self):
        if self.modules.get_is_preprocessed_files_used():
            print(Fore.RED + '💾 Preloaded files are used!' + Fore.RESET)
        else:
            print(Fore.RED + '📝 Importing and creating files' + Fore.RESET)

        oced_pg = self.modules.get_oced_pg()
        oced_pg.load_and_transform()
        oced_pg.create_df_edges()

    def finish_and_save(self):
        performance = self.modules.get_performance()
        performance.finish_and_save()

    def print_statistics(self):
        db_manager = self.modules.get_db_manager()
        db_manager.print_statistics()

    def close_connection(self):
        db_connection = self.modules.get_db_connection()
        db_connection.close_connection()
