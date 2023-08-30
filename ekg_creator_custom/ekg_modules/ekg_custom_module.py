from promg import DatabaseConnection
from promg import Performance
from ekg_creator_custom.cypher_queries.custom_query_library import CustomCypherQueryLibrary as ccql


class CustomModule:
    def __init__(self, db_connection: DatabaseConnection):
        self.connection = db_connection

    def do_custom_query(self, query_name, **kwargs):
        func = getattr(self, query_name)
        func(**kwargs)

    @Performance.track()
    def get_corr_between_o_created_events_and_offer_entities(self):
        self.connection.exec_query(ccql.get_corr_between_o_created_events_and_offer_entities)
