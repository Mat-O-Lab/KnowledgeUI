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

triplePath = os.path.join(baseDir1, 'data/EM_Graph.ttl')
graph = rdflib.Graph()
graph.parse(triplePath, format='n3')

# sparql = SPARQLWrapper("http://127.0.0.1:8080/fuseki/lebedigital")

prefixes = [
    '<{}https%3A//www.materials.fraunhofer.de/ontologies/BWMD_ontology/mid#>'.
    format(prefixPath),
    '<{}https%3A//purl.matolab.org/mseo/mid/>'.format(prefixPath),
    '<{}http%3A//www.ontologyrepository.com/CommonCoreOntologies/>'.format(
        prefixPath),
    '<{}http%3A//purl.obolibrary.org/obo/>'.format(prefixPath),
    '<{}https%3A//github.com/BAMresearch/ModelCalibration/blob/Datasets/usecases/Concrete/ConcreteOntology/Concrete_Ontology_MSEO.owl#>'
    .format(prefixPath)
]

dataPropertiesList = ['has_URI_value', 'has_text_value', 'has_decimal_value']


def get_name_from_uri(uri):
    i = uri.rfind('/') + 1
    name = uri[i:]
    return name


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
        results = graph.query(q1)

        for result in results:
            if sys.platform == 'win32':
                s.append(
                    get_name_from_uri(result['s'].value)
                    if result['s'].value != None else search)
                p.append(
                    get_name_from_uri(result['p'].value)
                    if result['p'].value != None else search)
                o.append(
                    get_name_from_uri(result['o'].value)
                    if result['o'].value != None else search)
            else:
                s.append(
                    get_name_from_uri(result['s']
                                      ) if result['s'] != None else search)
                p.append(
                    get_name_from_uri(result['p']
                                      ) if result['p'] != None else search)
                o.append(
                    get_name_from_uri(result['o']
                                      ) if result['o'] != None else search)

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
        results = graph.query(q1)

        for result in results:
            if sys.platform == 'win32':
                s.append(
                    get_name_from_uri(result['s'].value)
                    if result['s'].value != None else search)
                p.append(
                    get_name_from_uri(result['p'].value)
                    if result['p'].value != None else search)
                o.append(
                    get_name_from_uri(result['o'].value)
                    if result['o'].value != None else search)
            else:
                s.append(
                    get_name_from_uri(result['s']
                                      ) if result['s'] != None else search)
                p.append(
                    get_name_from_uri(result['p']
                                      ) if result['p'] != None else search)
                o.append(
                    get_name_from_uri(result['o']
                                      ) if result['o'] != None else search)

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
        results = graph.query(q1)

        for result in results:
            if sys.platform == 'win32':
                s.append(
                    get_name_from_uri(result['s'].value)
                    if result['s'].value != None else search)
                p.append(
                    get_name_from_uri(result['p'].value)
                    if result['p'].value != None else search)
                if get_name_from_uri(result['p']) in dataPropertiesList:
                    o.append(result['o'].value)
                else:
                    o.append(
                        get_name_from_uri(result['o'].value)
                        if result['o'].value != None else search)
            else:
                s.append(
                    get_name_from_uri(result['s']
                                      ) if result['s'] != None else search)
                p.append(
                    get_name_from_uri(result['p']
                                      ) if result['p'] != None else search)
                if get_name_from_uri(result['p']) in dataPropertiesList:
                    o.append(result['o'])
                else:
                    o.append(
                        get_name_from_uri(result['o']
                                          ) if result['o'] != None else search)

    df = pd.DataFrame({'s': s, 'p': p, 'o': o})
    return df