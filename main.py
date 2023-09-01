import os
from datetime import datetime
from pathlib import Path

from promg import SemanticHeader
from promg import EventKnowledgeGraph, DatabaseConnection
from promg import authentication
from promg import ImportedDataStructures

from promg import Performance
from ekg_creator_custom.ekg_modules.ekg_custom_module import CustomModule

# several steps of import, each can be switch on/off
from colorama import Fore

connection = authentication.connections_map[authentication.Connections.LOCAL]

dataset_name = 'BPIC14'
use_sample = True
batch_size = 100000
use_preprocessed_files = False

semantic_header_path = Path(f'json_files/{dataset_name}.json')
semantic_header = SemanticHeader.create_semantic_header(semantic_header_path)

perf_path = os.path.join("..", "perf", dataset_name, f"{dataset_name}_{'sample_' * use_sample}Performance.csv")

ds_path = Path(f'json_files/{dataset_name}_DS.json')
datastructures = ImportedDataStructures(ds_path)

step_clear_db = True
step_populate_graph = True

connection_key = authentication.Connections.LOCAL
verbose = False

def create_graph_instance() -> EventKnowledgeGraph:
    """
    Creates an instance of an EventKnowledgeGraph
    @return: returns an EventKnowledgeGraph
    """
    return EventKnowledgeGraph(batch_size=batch_size,
                               specification_of_data_structures=datastructures,
                               use_sample=use_sample,
                               use_preprocessed_files=use_preprocessed_files,
                               semantic_header=semantic_header,
                               perf_path=perf_path,
                               custom_module_name=CustomModule)


def clear_graph(graph: EventKnowledgeGraph) -> None:
    """
    # delete all nodes and relations in the graph to start fresh
    @param graph: EventKnowledgeGraph
    @param perf: Performance
    @return: None
    """

    print("Clearing DB...")
    graph.clear_db()


def populate_graph(graph: EventKnowledgeGraph):
    # TODO: constraints in semantic header?
    graph.set_constraints()

    graph.create_static_nodes_and_relations()

    # import the events from all sublogs in the graph with the corresponding labels
    graph.import_data()

    # for each entity, we add the entity nodes to graph and correlate them to the correct events
    graph.create_nodes_by_records()

    # for each relation, we add the entity nodes to graph and correlate them to the correct events
    graph.create_relations()

    # graph.create_nodes_by_relations()

    # graph.create_df_edges()

    # graph.delete_parallel_dfs_derived()

    # graph.merge_duplicate_df()


def main() -> None:
    """
    Main function, read all the logs, clear and create the graph, perform checks
    @return: None
    """
    print("Started at =", datetime.now().strftime("%H:%M:%S"))

    db_connection = DatabaseConnection.set_up_connection_using_key(key=connection_key,
                                                                   verbose=verbose)

    if use_preprocessed_files:
        print(Fore.RED + '💾 Preloaded files are used!' + Fore.RESET)
    else:
        print(Fore.RED + '📝 Importing and creating files' + Fore.RESET)

    # performance class to measure performance
    graph = create_graph_instance()

    if step_clear_db:
        clear_graph(graph=graph)

    if step_populate_graph:
        populate_graph(graph=graph)

    graph.save_perf()
    graph.print_statistics()

    db_connection.close_connection()


if __name__ == "__main__":
    main()
