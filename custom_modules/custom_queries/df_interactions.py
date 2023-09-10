from dataclasses import dataclass
from typing import Dict, Optional, Union

from string import Template

from promg import Query
from promg.data_managers.semantic_header import ConstructedNodes, ConstructedRelation


class InferDFInteractionsQueryLibrary:
    @staticmethod
    def delete_parallel_directly_follows_derived(entity: Union[ConstructedNodes, ConstructedRelation],
                                                 original_entity: Union[ConstructedNodes, ConstructedRelation],
                                                 event_label: str = 'Event'):
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
                         "df_entity": entity.get_df_label(),
                         "df_original_entity": original_entity.get_df_label(),
                         "event_label": event_label
                     })
