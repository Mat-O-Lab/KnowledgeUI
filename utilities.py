import json
import requests
from io import StringIO
import pandas as pd

def fetch_overview_data(ENDPOINT):
    """ Fetches an overview of the class hierarchies of the specified triples store.
    """
    query = """
            PREFIX owl: <http://www.w3.org/2002/07/owl#>
            PREFIX rdf: <http://www.w3.org/1999/02/22-rdf-syntax-ns#>
            PREFIX rdfs: <http://www.w3.org/2000/01/rdf-schema#>
            SELECT ?c (MIN(?label) AS ?label1) ?superclass (count(?x) as ?count) WHERE {
            SERVICE <https://fuseki.matolab.org/alutrace/sparql> {
                ?x a ?c.
                ?c rdfs:label ?label.
                ?c rdfs:subClassOf ?superclass.
                filter (?c != ?superclass &&
                        !exists {?c rdfs:subClassOf ?othersuper. ?othersuper rdfs:subClassOf ?superclass.
                                filter(?c != ?othersuper && ?othersuper != ?superclass)})
            }
            } group by ?c ?label1 ?superclass HAVING(?count > 1) order by desc(?count)
            """

    return requests.get(ENDPOINT, params={'query': query}, headers={'Accept': 'text/csv'}).text



def parse_sunburst(csv: str):
    """ Converts a class hierarchy csv dataset into a hierarchical JSON format.
    """
    reverse_dict = {}
    # go through each line of results, excluding the header

    for line in csv.split('\n')[1:-1]:
        if len(line.split(','))==4:
            iri, label, parent, count = [elem.strip() for elem in line.split(',')]
        try:
            reverse_dict[parent].append({'iri': iri, 'label': label, 'count': count})
        except KeyError:
            reverse_dict[parent] = [{'iri': iri, 'label': label, 'count': count}]

    #base_node = {'iri': 'http://www.w3.org/2002/07/owl#Thing', 'label': 'Thing'}
    base_node = {'iri': 'http://purl.obolibrary.org/obo/BFO_0000001', 'label': 'Entity'}

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
    json_obj = json.loads(json_data)
    csv_rows = [','.join(json_obj['columns'])] + [','.join([elem['uri'] for elem in row]) for row in json_obj['rows']]
    dataframe = pd.read_csv(StringIO('\n'.join(csv_rows)))
    return dataframe
