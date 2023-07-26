from promg import DatabaseConnection
from promg import Performance
from ekg_creator_custom.cypher_queries.custom_query_library import CustomCypherQueryLibrary as ccql


class CustomModule:
    def __init__(self, db_connection: DatabaseConnection, perf: Performance):
        self.connection = db_connection
        self.perf = perf

    def _write_message_to_performance(self, message: str):
        if self.perf is not None:
            self.perf.finished_step(activity=message)

    def do_custom_query(self, query_name, **kwargs):
        func = getattr(self, query_name)
        func(**kwargs)

    def get_corr_between_o_created_events_and_offer_entities(self):
        self.connection.exec_query(ccql.get_corr_between_o_created_events_and_offer_entities)
