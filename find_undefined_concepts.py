#!/usr/bin/env python
"""
Find all of the undefined concepts in a target ontology.
"""

import os
from rdflib import Graph, util

# Load the provided SPARQL queries from the respective files
with open("./queries/defined_concept_query.rq", "r") as file:
    defined_concept_query = file.read()

with open("./queries/undefined_concept_query_template.rq", "r") as file:
    undefined_concept_query_template = file.read()


def create_defined_concepts(combined_graph):
    """Create the list of concepts that are defined in the ontologies provided"""
    return [str(row['defined_iri']) for row in combined_graph.query(defined_concept_query)]


def find_undefined_concepts(defined_concepts_list, graph_of_interest):
    """Function to find undefined concepts"""
    # Convert each IRI to its SPARQL format and join into a single string separated by commas
    formatted_defined_concepts = ", ".join([f"<{iri}>" for iri in defined_concepts_list])

    # Injecting the formatted concepts into the query template
    undefined_concept_query_final = undefined_concept_query_template.replace("##DEFINED_CONCEPTS##", formatted_defined_concepts)

    # Use the updated undefined_concept_query to find undefined concepts
    rows = graph_of_interest.query(undefined_concept_query_final)
    if len(rows) == 0:
        return
    print("\nUndefined concepts:")
    for row in rows:
        print(row["undefined_concept"])
    print('\n')


def add_files_to_graph(rdf_file, combined_graph, graph_of_interest = None):
    """"
    Adds files to the combined graph, if a graph of interest is passed in, will also add that to the graph of interest.
    This returns the combined_graph and the graph of interest. If you don't need the graph of interest, don't try to capture it

    Use like  `combined_graph, _ = add_files_to_graph(rdf_file, combined_graph)`
    Or `combined_graph, graph_of_interest = add_files_to_graph(rdf_file, combined_graph, graph_of_interest)`

    These are combined into a single function because of the overlap between populating these graphs

    """
    fmt = util.guess_format(rdf_file)
    if not fmt:
        print(f"{rdf_file} does not have a parsable extension, and will not be added to the graph.\n")
        return
    combined_graph.parse(rdf_file, format=fmt)
    if graph_of_interest != None:
        graph_of_interest.parse(rdf_file, format=fmt)
    return combined_graph, graph_of_interest


def main():
    """Handle the command line arguments for the operation of comments"""
    # Set up command-line argument parsing for only the graph
    parser = argparse.ArgumentParser(description='Process and query ontologies.')
    parser.add_argument('-c', '--context', nargs="*", help='Path to imported or context rdf files or directories.')
    parser.add_argument('focus_graph', nargs="+", help='Path to the RDF graphs of interest (.ttl file, or any file in rdf format with a proper extension). These are the graphs we are interested in seeing undefined concepts')
    args = parser.parse_args()

    # Load the graph of interest from the specified file
    combined_graph = Graph()
    graph_of_interest = Graph()
    # load the focus graph, the graph
    for rdf_file in args.focus_graph:
        combined_graph, graph_of_interest = add_files_to_graph(rdf_file, combined_graph, graph_of_interest)

    for context in args.context:
        if os.path.isfile(context):
            combined_graph, _ = add_files_to_graph(context, combined_graph)
        elif os.path.isdir(context):
            full_path = os.path.abspath(context)
            for rdf_file in os.listdir(context):
                combined_graph, _ = add_files_to_graph(os.path.join(full_path, rdf_file), combined_graph)
        else:
           print(f"there is an error with {context}")

    defined_concepts = create_defined_concepts(combined_graph)

    find_undefined_concepts(defined_concepts, graph_of_interest)

if __name__ == '__main__':
    import argparse

    main()
