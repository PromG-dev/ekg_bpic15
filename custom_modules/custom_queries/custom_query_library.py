from dataclasses import dataclass
from typing import Dict, Optional

from string import Template

from promg import Query


class CustomCypherQueryLibrary:
    @staticmethod
    def get_example_query(labels: str):
        query_str = '''
            MATCH (n:$labels)
            RETURN count(n)
        '''

        return Query(query_str=query_str,
                     template_string_parameters={
                        "labels": labels
        })