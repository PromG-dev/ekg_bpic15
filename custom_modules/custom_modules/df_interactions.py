from promg import DatabaseConnection, SemanticHeader
from promg import Performance
from custom_modules.custom_queries.df_interactions import InferDFInteractionsQueryLibrary as ql


class InferDFInteractions:
    def __init__(self):
        self.connection = DatabaseConnection()
        
    @Performance.track()
    def delete_parallel_directly_follows_derived(self, entity_str:str,original_entity_str:str):
        entity = SemanticHeader().get_entity(entity_type=entity_str)
        original_entity = SemanticHeader().get_entity(entity_type=original_entity_str)

        self.connection.exec_query(ql.delete_parallel_directly_follows_derived,
                                   **{
                                        "entity": entity,
                                        "original_entity": original_entity
                                   })