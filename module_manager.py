from promg import SemanticHeader, OcedPg
from promg import DatabaseConnection
from promg import DatasetDescriptions

from promg import Performance
from promg.modules.db_management import DBManagement
from promg import Configuration


class ModuleManager:
    def __init__(self, config):
        if config is None:
            config = Configuration.init_conf_with_config_file()
        self._config = config
        self._db_connection = DatabaseConnection.set_up_connection(config=config)
        self._performance = Performance.set_up_performance(config=config)
        self._semantic_header = SemanticHeader.create_semantic_header(config=config)
        self._dataset_descriptions = DatasetDescriptions(config=config)

        self._db_manager = None
        self._oced_pg = None

    def get_config(self):
        return self._config

    def get_is_preprocessed_files_used(self):
        return self._config.use_preprocessed_files
    def get_db_connection(self):
        return self._db_connection

    def get_performance(self):
        return self._performance

    def get_db_manager(self):
        if self._db_manager is None:
            self._db_manager = DBManagement(db_connection=self._db_connection)
        return self._db_manager

    def get_oced_pg(self):
        if self._oced_pg is None:
            self._oced_pg = OcedPg(database_connection=self._db_connection,
                                   dataset_descriptions=self._dataset_descriptions,
                                   semantic_header=self._semantic_header,
                                   use_sample=self._config.use_sample,
                                   use_preprocessed_files=self._config.use_preprocessed_files)
        return self._oced_pg
