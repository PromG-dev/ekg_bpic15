from dataclasses import dataclass
from typing import Dict, Optional

from string import Template

from promg import Query


class InferDFInteractionsQueryLibrary:

    @staticmethod
    def create_df_edges_for_relations(entity_labels:str,corr_type:str,df_entity:str,entity_type:str,event_label:str='Event'):
        query_str = '''
                        CALL apoc.periodic.iterate(
                        'MATCH (n:$entity_labels_string) <-[:$corr_type_string]- (e:$event_label)
                        WITH n , e as nodes ORDER BY e.timestamp, ID(e)
                        WITH n , collect (nodes) as nodeList
                        UNWIND range(0,size(nodeList)-2) AS i
                        WITH n , nodeList[i] as first, nodeList[i+1] as second
                        RETURN first, second',
                        'MERGE (first) -[df:$df_entity {entityType: "$entity_type"}]->(second)
                            SET df.type = "DF"
                        ',
                        {batchSize: $batch_size})
                    '''

        return Query(query_str=query_str,
                     template_string_parameters={
                         "entity_labels_string": entity_labels,
                         "corr_type_string": corr_type,
                         "event_label": event_label,
                         "df_entity": df_entity,
                         "entity_type": entity_type
                     })

    @staticmethod
    def delete_parallel_directly_follows_derived(df_entity:str,df_original_entity:str,event_label:str='Event'):
        query_str = '''
                        CALL apoc.periodic.iterate(
                        'MATCH (e1:$event_label) -[df:$df_entity]-> (e2:$event_label)
                         WHERE (e1) -[:$df_original_entity]-> (e2)
                         RETURN df',
                        'WITH df DELETE df
                        ',
                        {batchSize: $batch_size})
                    '''

        return Query(query_str=query_str,
                     template_string_parameters={
                         "df_entity": df_entity,
                         "df_original_entity": df_original_entity,
                         "event_label": event_label
                     })
    