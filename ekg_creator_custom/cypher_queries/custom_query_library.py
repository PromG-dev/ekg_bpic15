from dataclasses import dataclass
from typing import Dict, Optional

from string import Template


@dataclass
class Query:
    query_string: str
    kwargs: Optional[Dict[str, any]]


class CustomCypherQueryLibrary:
    @staticmethod
    def get_corr_between_o_created_events_and_offer_entities():
        query_str = '''
            MATCH (e:Event {activity:"O_Created"}) - [:CORR] -> (o:Offer)
            CALL {
                WITH e
                MATCH (f:Event)
                WHERE f.timestamp <= e.timestamp AND e <> f AND e.log = f.log
                RETURN f
                ORDER BY f.timestamp DESCENDING
                LIMIT 1
            }
            WITH o, e, f
            WHERE f.activity = "O_Create Offer"
            MERGE (f) - [:CORR] -> (o)
        '''

        return Query(query_string=query_str, kwargs={})