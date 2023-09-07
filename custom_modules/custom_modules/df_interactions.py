from promg import DatabaseConnection
from promg import Performance
from custom_modules.custom_queries.df_interactions import InferDFInteractionsQueryLibrary as ql


class InferDFInteractions:
    def __init__(self):
        self.connection = DatabaseConnection()

    @Performance.track()
    def create_df_edges_for_relations(self, entity_labels:str,df_entity:str,entity_type:str,corr_type:str='CORR'):
        self.connection.exec_query(ql.create_df_edges_for_relations,
                                   **{
                                       "entity_labels": entity_labels,
                                       "corr_type": corr_type,
                                       "df_entity": df_entity,
                                       "entity_type": entity_type
                                   })
        
    @Performance.track()
    def delete_parallel_directly_follows_derived(self, df_entity:str,df_original_entity:str):
        self.connection.exec_query(ql.delete_parallel_directly_follows_derived,
                                   **{
                                        "df_entity": df_entity,
                                        "df_original_entity": df_original_entity
                                   })