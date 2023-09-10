from promg import DatabaseConnection
from promg import Performance
from custom_modules.custom_queries.delay_analysis import PerformanceAnalyzeDelaysQueryLibrary as ql


class PerformanceAnalyzeDelays:
    def __init__(self):
        self.connection = DatabaseConnection()

    @Performance.track()
    def enrich_with_delay_edges(self):
        result = self.connection.exec_query(ql.q_create_delay_edges)
        print(f"Computed {result} delay edges.")

    @Performance.track()
    def analyze_delays(self):
        result = self.connection.exec_query(ql.q_summarize_delay_entities)
        for r in result:
            print(f"{r['delay_by']} delayed an activity {r['frequency']} times.")

    @Performance.track()
    def visualize_delays(self,threshold:int=0):
        self.connection.exec_query(ql.visualize_delays,
                                   **{
                                       "threshold": threshold
                                   })
