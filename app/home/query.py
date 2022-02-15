from SPARQLWrapper import SPARQLWrapper, JSON
from xml.dom.minidom import NamedNodeMap
import rdflib
from SPARQLWrapper import SPARQLWrapper
import os
from pathlib import Path
import sys
import pandas as pd

baseDir0 = Path(__file__).resolve().parents[0]
baseDir1 = Path(__file__).resolve().parents[1]
baseDir2 = Path(__file__).resolve().parents[2]

if sys.platform == 'win32':
    prefixPath = 'file:///' + os.path.join(baseDir1, 'data').replace(
        '\\', '/') + '/'
else:
    prefixPath = 'file://' + os.path.join(baseDir1, 'data') + '/'

"""triplePath = os.path.join(baseDir1, 'data/EM_Graph.ttl')
graph = rdflib.Graph()
graph.parse(triplePath, format='n3')"""

#We just need to change the name with the actual database to be useds
sparql = SPARQLWrapper("https://dataconnect.bam.de/graph/lebedigital-emodul/query")

prefixes = [
    '<https://www.materials.fraunhofer.de/ontologies/BWMD_ontology/mid#>',
    '<https://purl.matolab.org/mseo/mid/>',
    '<http://www.ontologyrepository.com/CommonCoreOntologies/>',
    '<http://purl.obolibrary.org/obo/>',
    '<https://github.com/BAMresearch/ModelCalibration/blob/Datasets/usecases/Concrete/ConcreteOntology/Concrete_Ontology_MSEO.owl#>',
    '<http://www.w3.org/2002/07/>'
]

dataPropertiesList = ['has_URI_value', 'has_text_value', 'has_decimal_value']

def get_name_from_uri(uri):
    i = uri.rfind('/') + 1
    name = uri[i:]
    return name

def send_query(q1):
    sparql.setQuery(q1)
    sparql.setReturnFormat(JSON)
    return sparql.query().convert()

def search_string(search):

    try:
        search = search.replace(' ', '_').replace('.', '_')
    except:
        search = search
    # else:
    #     try:

    #         search = "{:e}".format(search)
    #     except:
    #         search = search
    s = []
    p = []
    o = []
    for pref in prefixes:

        q1 = f"""
                prefix pf: {pref}
                
                select ?s ?p ?o
                where {{
                    {{
                        pf:{search}
                        ?p
                        ?o
                    }}
                    union
                    {{
                        ?s
                        ?p
                        pf:{search}
                    }}
                    
                    union
                    {{
                        "{search}"
                        ?p
                        ?o
                    }}
                    union
                    {{
                        ?s
                        ?p
                        "{search}"
                    }}
                }}
         """
        results = send_query(q1)

        for result in results['results']['bindings']:
            if sys.platform == 'win32':
                s.append(
                    get_name_from_uri(result['s']['value'])
                    if 's' in result else search)
                p.append(
                    get_name_from_uri(result['p']['value'])
                    if 'p' in result else search)
                o.append(
                    get_name_from_uri(result['o']['value'])
                    if 'o' in result  else search)
            else:
                s.append(
                    get_name_from_uri(result['s']['value']
                                      )if 's' in result else search)
                p.append(
                    get_name_from_uri(result['p']['value']
                                      ) if 'p' in result else search)
                o.append(
                    get_name_from_uri(result['o']['value']
                                      ) if 'o' in result else search)

    df = pd.DataFrame({'s': s, 'p': p, 'o': o})
    return df


def search_number(search):
    search = "{:e}".format(search)
    s = []
    p = []
    o = []
   
    for pref in prefixes:

        q1 = f"""
                prefix pf: {pref}
                
                select ?s ?p ?o
                where {{
                    
                    {{
                        {search}
                        ?p
                        ?o
                    }}
                    union
                    {{
                        ?s
                        ?p
                        {search}
                    }}
                }}
            """
        results = send_query(q1)
        for result in results['results']['bindings']:
            if sys.platform == 'win32':
                s.append(
                    get_name_from_uri(result['s']['value'])
                    if 's' in result else search)
                p.append(
                    get_name_from_uri(result['p']['value'])
                    if 'p' in result else search)
                o.append(
                    get_name_from_uri(result['o']['value'])
                    if 'o' in result  else search)
            else:
                s.append(
                    get_name_from_uri(result['s']['value']
                                      )if 's' in result else search)
                p.append(
                    get_name_from_uri(result['p']['value']
                                      ) if 'p' in result else search)
                o.append(
                    get_name_from_uri(result['o']['value']
                                      ) if 'o' in result else search)

    df = pd.DataFrame({'s': s, 'p': p, 'o': o})
    return df


def continue_string_search(search):
    try:
        search = search.replace(' ', '_').replace('.', '_')
    except:
        search = search

    # else:
    #     try:

    #         search = "{:e}".format(search)
    #     except:
    #         search = search
    s = []
    p = []
    o = []
    for pref in prefixes:

        q1 = f"""
                prefix pf: {pref}
                
                select ?s ?p ?o
                where {{
                    {{
                        pf:{search}
                        ?p
                        ?o
                    }}
                    union
                    {{
                        ?s
                        ?p
                        pf:{search}
                    }}
                    
                    union
                    {{
                        "{search}"
                        ?p
                        ?o
                    }}
                    union
                    {{
                        ?s
                        ?p
                        "{search}"
                    }}
                }}
            """
        results = send_query(q1)

        for result in results['results']['bindings']:
            if sys.platform == 'win32':
                s.append(
                    get_name_from_uri(result['s']['value'])
                    if 's' in result else search)
                p.append(
                    get_name_from_uri(result['p']['value'])
                    if 'p' in result else search)
                if get_name_from_uri(result['p']['value']) in dataPropertiesList:
                    o.append(result['o']['value'])
                else:
                    o.append(
                        get_name_from_uri(result['o']['value'])
                        if 'o' in result else search)
            else:
                s.append(
                    get_name_from_uri(result['s']['value']
                                      ) if 's' in result else search)
                p.append(
                    get_name_from_uri(result['p']['value']
                                      ) if 'p' in result else search)
                if get_name_from_uri(result['p']['value']) in dataPropertiesList:
                    o.append(result['o']['value'])
                else:
                    o.append(
                        get_name_from_uri(result['o']['value']
                                          ) if 'o' in result else search)

    df = pd.DataFrame({'s': s, 'p': p, 'o': o})
    return df

#Allows to get a list with all the occurencies in the DB
#For the moment s, p ans o in the same list and doing that only once
def initAutocompleteList():
    results = send_query("""
        prefix rdfs: <http://www.w3.org/2000/01/rdf-schema#>
        prefix owl: <http://www.w3.org/2002/07/owl#>

        SELECT ?wanted (count(?wanted) AS ?count)
        WHERE {
        ?material ?wanted ?object .
        }
        GROUP BY ?wanted
        ORDER BY ?count
    """)

    results1 = send_query("""
        prefix rdfs: <http://www.w3.org/2000/01/rdf-schema#>
        prefix owl: <http://www.w3.org/2002/07/owl#>

        SELECT ?wanted (count(?wanted) AS ?count)
        WHERE {
         ?wanted ?p ?object .
        }
        GROUP BY ?wanted
        ORDER BY ?count
        """)

    results2 = send_query("""
        prefix rdfs: <http://www.w3.org/2000/01/rdf-schema#>
        prefix owl: <http://www.w3.org/2002/07/owl#>

        SELECT ?wanted (count(?wanted) AS ?count)
        WHERE {
        ?s ?p ?wanted .
        }
        GROUP BY ?wanted
        ORDER BY ?count
    """)

    l = list()
    for s in results1["results"]["bindings"]:
        l.append(get_name_from_uri(s['wanted']['value']))
    for s in results["results"]["bindings"]:
        l.append(get_name_from_uri(s['wanted']['value']))
    for s in results2["results"]["bindings"]:
        l.append(get_name_from_uri(s['wanted']['value']))
    return l
    