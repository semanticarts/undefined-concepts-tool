#!/usr/bin/env python

import os
import argparse
from rdflib import Graph

# Set up command-line argument parsing for only the graph
parser = argparse.ArgumentParser(description='Process and query ontologies.')
parser.add_argument('graph_path', type=str, help='Path to the RDF graph of interest (.ttl file).')
args = parser.parse_args()

# Load the graph of interest from the specified file
graph_of_interest = Graph()
graph_of_interest.parse(args.graph_path, format='turtle')

# Load the provided SPARQL queries from the respective files
with open("./queries/defined_concept_query.rq", "r") as file:
    defined_concept_query = file.read()

with open("./queries/undefined_concept_query_template.rq", "r") as file:
    undefined_concept_query_template = file.read()

# Function to combine ontologies and generate a list of defined concepts
def combine_ontologies():
    
    combined_graph_path = "./ontologies/combinedGraph.ttl"
    defined_concepts_txt_path = './defined_concepts.txt'
    
    if os.path.exists(combined_graph_path):
        os.remove(combined_graph_path)
    
    if os.path.exists(defined_concepts_txt_path):
        os.remove(defined_concepts_txt_path)

    combinedGraph = Graph()
    ttl_dir = './ontologies'
    for filename in os.listdir(ttl_dir):
        if filename.endswith('.ttl'):
            ttl_path = os.path.join(ttl_dir, filename)
            combinedGraph.parse(ttl_path, format='turtle')

    combinedGraph.serialize(destination="./ontologies/combinedGraph.ttl")
    
    # Use the defined_concept_query to extract defined concepts
    defined_concepts_list = []
    for row in combinedGraph.query(defined_concept_query):
        defined_concepts_list.append(str(row['defined_iri']))
    
    with open('./defined_concepts.txt', 'w') as f:
        f.write('\n'.join(defined_concepts_list))
    
    return defined_concepts_list

# Function to find undefined concepts
def find_undefined_concepts(defined_concepts_list):
    # Convert each IRI to its SPARQL format and join into a single string separated by commas
    formatted_defined_concepts = ", ".join([f"<{iri}>" for iri in defined_concepts_list])
    
    # Injecting the formatted concepts into the query template
    undefined_concept_query_final = undefined_concept_query_template.replace("##DEFINED_CONCEPTS##", formatted_defined_concepts)

    # Use the updated undefined_concept_query to find undefined concepts
    print("\nUndefined concepts:")
    for row in graph_of_interest.query(undefined_concept_query_final):
        print(row["undefined_concept"])
    print('\n')

if __name__ == '__main__':
    find_undefined_concepts(combine_ontologies())
