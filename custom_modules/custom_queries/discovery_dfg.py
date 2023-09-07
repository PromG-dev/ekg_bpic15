from dataclasses import dataclass
from typing import Dict, Optional

from string import Template

from promg import Query


class DiscoverDFGQueryLibrary:

    @staticmethod
    def aggregate_df_relations_heuristic(df_label:str,corr_label:str,dfc_label:str,df_threshold:int,relative_df_threshold:float,event_label:str='Event'):
        query_str = '''
                        MATCH
                        (c1:Activity) 
                            -[:OBSERVED]->
                        (e1:$event_label) -[df:$df_label]-> (e2:$event_label) 
                            <-[:OBSERVED]-
                        (c2:Activity)
                        MATCH (e1) -[:$corr_label] -> (n) <-[:$corr_label]- (e2)
                        WITH c1,count(df) AS df_freq,c2
                        WHERE df_freq > $df_threshold
                        OPTIONAL MATCH (c2) -[:OBSERVED]-> (e2b:$event_label) -[df2:$df_label]->(e1b:$event_label) <-[:OBSERVED]- (c1)
                        WITH c1,df_freq,count(df2) AS df_freq2,c2
                        WHERE (df_freq > df_freq2 * $relative_df_threshold)
                        MERGE (c1)-[rel2:$dfc_label {type:'DF_A'}]->(c2) 
                        ON CREATE SET rel2.count=df_freq
                    '''

        return Query(query_str=query_str,
                     template_string_parameters={
                         "corr_label": corr_label,
                         "event_label": event_label,
                         "df_label": df_label,
                         "dfc_label": dfc_label,
                         "df_threshold": df_threshold,
                         "relative_df_threshold": relative_df_threshold
                     })

    @staticmethod
    def aggregate_df_relations(df_label:str,corr_label:str,dfc_label:str,df_threshold:int,event_label:str='Event'):
        query_str = '''
                        MATCH
                        (c1:Activity) 
                            -[:OBSERVED]->
                        (e1:$event_label) -[df:$df_label]-> (e2:$event_label) 
                            <-[:OBSERVED]-
                        (c2:Activity)
                        MATCH (e1) -[:$corr_label] -> (n) <-[:$corr_label]- (e2)
                        WITH c1,count(df) AS df_freq,c2
                        WHERE df_freq > $df_threshold
                        MERGE (c1)-[rel2:$dfc_label {type:'DF_A'}]->(c2) 
                        ON CREATE SET rel2.count=df_freq
                    '''

        return Query(query_str=query_str,
                     template_string_parameters={
                         "corr_label": corr_label,
                         "event_label": event_label,
                         "df_label": df_label,
                         "dfc_label": dfc_label,
                         "df_threshold": df_threshold
                     })
