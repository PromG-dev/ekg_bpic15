from dataclasses import dataclass
from typing import Dict, Optional

from string import Template

from promg import Query


class PerformanceAnalyzeDelaysQueryLibrary:
    @staticmethod
    def q_create_delay_edges():
        query_str = '''
            MATCH (e1:Event)-[df {type:"DF"}]->(e2:Event) WHERE df.entityType <> 'CaseAWO'
            WITH e1,e2 ORDER BY duration.between(e1.timestamp,e2.timestamp)
            WITH collect(e1)[0] as e1_last,e2
            MATCH (e1_last)-[df {type:"DF"}]->(e2:Event) WHERE df.entityType <> 'CaseAWO'
            MERGE (e1_last)-[delay:DELAY]->(e2) ON CREATE SET delay.by=df.entityType
            RETURN count(delay) AS delay_edges
        '''

        return Query(query_str=query_str)
    

    @staticmethod
    def q_summarize_delay_entities():
        query_str = '''
            MATCH (e1:Event)-[delay:DELAY]->(e2:Event)
            RETURN delay.by AS delay_by,count(delay) AS frequency
        '''
        return Query(query_str=query_str)
    

    @staticmethod
    def visualize_delays(threshold:int,event_label:str='Event'):
        query_str = '''
                        MATCH
                        (c1:Activity) 
                            -[:OBSERVED]->
                        (e1:$event_label) -[delay:DELAY]-> (e2:$event_label) 
                            <-[:OBSERVED]-
                        (c2:Activity)
                        WITH c1, delay.by AS delay_by, c2, count(delay) AS delay_freq
                        WHERE delay_freq > $threshold
                        MERGE (c1)-[rel2:DELAY_A]->(c2) 
                        ON CREATE SET rel2.count=delay_freq, rel2.by=delay_by
                    '''

        return Query(query_str=query_str,
                     template_string_parameters={
                         "event_label": event_label,
                         "threshold": threshold
                     })
