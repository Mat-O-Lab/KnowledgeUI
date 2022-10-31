import json
from multiprocessing.sharedctypes import Value
from turtle import pos
from typing import Set
import requests
from sklearn import datasets
import os

from rdflib import URIRef

from io import StringIO
import pandas as pd

def fetch_overview_data(endpoint):
    """ Fetches an overview of the class hierarchies of the specified triples store.
    """
    user_defined_query = None
    query = """
            PREFIX owl: <http://www.w3.org/2002/07/owl#>
            PREFIX rdf: <http://www.w3.org/1999/02/22-rdf-syntax-ns#>
            PREFIX rdfs: <http://www.w3.org/2000/01/rdf-schema#>
            SELECT ?c (MIN(?label) AS ?label1) ?superclass (count(?x) as ?count) WHERE {
            SERVICE <""" + endpoint + """> {
                ?x a ?c.
                ?c rdfs:label ?label.
                ?c rdfs:subClassOf ?superclass.
                filter (?c != ?superclass &&
                        !exists {?c rdfs:subClassOf ?othersuper. ?othersuper rdfs:subClassOf ?superclass.
                                filter(?c != ?othersuper && ?othersuper != ?superclass)})
            }
            } group by ?c ?label1 ?superclass HAVING(?count > 1) order by desc(?count)
            """
    """
    define a default dataset in case the expected one is not accessible
    or database is down
    """
    try:
        response = requests.get(endpoint, params={'query': query}, headers={'Accept': 'text/csv'})
        response.raise_for_status()
        return response.text
    except requests.exceptions.HTTPError as err:
        raise requests.HTTPError(err)




def parse_sunburst(csv: str):
    """ Converts a class hierarchy csv dataset into a hierarchical JSON format.
    """
    reverse_dict = {}
    parents = set()
    iris = set()
    # go through each line of results, excluding the header

    for line in csv.split('\n')[1:-1]:
        elems = line.split(',')
        if len(elems)==4:
            iri, label, parent, count = [elem.strip() for elem in elems]
            parents.add(parent)
            iris.add(iri)
        else:
            raise RuntimeError("No 4 elements in csv line!")
        try:
            reverse_dict[parent].append({'iri': iri, 'label': label, 'count': count})
        except KeyError:
            reverse_dict[parent] = [{'iri': iri, 'label': label, 'count': count}]

    possible_parents = parents - iris
    
    # if there are more than one possible parenty, try to find the one that has Thing in it
    if len(possible_parents) > 1:
        use_parent = [elem for elem in list(possible_parents) if 'Thing' in elem]
    else:
        use_parent = list(possible_parents)
    
    base_node = {'iri': use_parent[0], 'label': use_parent[0], 'count': 1}
    #base_node = {'iri': 'http://www.w3.org/2002/07/owl#Thing', 'label': 'Thing'}

    return json.dumps(__make_children(base_node, reverse_dict))

def __make_children(node, reverse_dict):
    obj = {'name': node['label'], 'iri': node['iri']}
    if node['iri'] in reverse_dict:
        children = []
        for child in reverse_dict[node['iri']]:
            children.append(__make_children(child, reverse_dict))
        obj['children'] = children
    else:
        obj['size'] = node['count']
    
    return obj

def parse_json_string_to_df(json_data):
    #print(json_data)
    json_obj = json.loads(json_data)
    print(json_obj)
    csv_rows = [','.join(json_obj['columns'])] + [','.join(row) for row in json_obj['rows']]
    dataframe = pd.read_csv(StringIO('\n'.join(csv_rows)))
    return dataframe
