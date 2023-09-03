from promg import DatabaseConnection
from promg import Performance
from custom_modules.custom_queries.custom_query_library import CustomCypherQueryLibrary as ccql


class CustomModule:
    def __init__(self):
        self.connection = DatabaseConnection()

    @Performance.track()
    def test_query(self):
        result = self.connection.exec_query(ccql.get_example_query,
                                   **{"labels": "Entity:Offer"})
        print(f"Total amount of (:Entity:Offer) nodes = {result}")
