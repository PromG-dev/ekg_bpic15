from promg import DatabaseConnection
from promg import Performance
from custom_modules.custom_queries.discovery_dfg import DiscoverDFGQueryLibrary as ql


class DiscoverDFG:
    def __init__(self):
        self.connection = DatabaseConnection()

    @Performance.track()
    def discover_dfg_for_entity(self, df_label:str,dfc_label:str,df_threshold:int=0,relative_df_threshold:float=0.0,corr_label:str='CORR'):
        if relative_df_threshold==0.0:
            self.connection.exec_query(ql.aggregate_df_relations,
                                    **{
                                            "corr_label": corr_label,
                                            "df_label": df_label,
                                            "dfc_label": dfc_label,
                                            "df_threshold": df_threshold
                                        })
        else:
            self.connection.exec_query(ql.aggregate_df_relations_heuristic,
                                    **{
                                            "corr_label": corr_label,
                                            "df_label": df_label,
                                            "dfc_label": dfc_label,
                                            "df_threshold": df_threshold,
                                            "relative_df_threshold": relative_df_threshold
                                        })
