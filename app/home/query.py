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

#We just need to change the name with the actual database to be useds
sparql = SPARQLWrapper("https://dataconnect.bam.de/graph/lebedigital-emodul/query")

classPrefixDic = dict()

prefixes = [
            '<http://www.w3.org/2002/07/owl#>',
            '<https://www.materials.fraunhofer.de/ontologies/graph_designer#>',
            '<http://purl.org/dc/terms/>',
            '<http://www.ontologyrepository.com/CommonCoreOntologies/>',
            '<http://purl.obolibrary.org/obo/>',
            '<http://www.geneontology.org/formats/oboInOwl#>',
            '<http://www.daml.org/2003/01/periodictable/PeriodicTable#>',
            '<http://www.ontologyrepository.com/CommonCoreOntologies/>',
            '<http://purl.obolibrary.org/obo/>',
            '<http://purl.org/dc/elements/1.1/>',
            '<https://www.materials.fraunhofer.de/ontologies/BWMD_ontology/mid#>',
            '<http://www.w3.org/1999/02/22-rdf-syntax-ns#>',
            '<http://www.w3.org/2000/01/rdf-schema#>',
            '<http://www.w3.org/2001/XMLSchema#>',
            '<https://purl.matolab.org/mseo/mid/>'
]

dataPropertiesList = ['has_URI_value', 'has_text_value', 'has_decimal_value']

def get_name_from_uri(uri):
    i = uri.rfind('/') + 1
    k = uri.rfind('#') + 1

    name = uri[i:] if k < i else uri[k:]
    return name

def get_prefix_from_uri(uri):
    i = uri.rfind('/') + 1
    k = uri.rfind('#') + 1

    pf = uri[:i] if k < i else uri[:k]
    return pf

def send_query(q1):
    sparql.setQuery(q1)
    sparql.setReturnFormat(JSON)
    return sparql.query().convert()

def search_instances(search):

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
                        ?s
                        a
                        pf:{search}
                    }} 
                    union
                    {{
                        ?s
                        a   
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
                p.append("a")
                o.append(
                    get_name_from_uri(result['o']['value'])
                    if 'o' in result  else search)
            else:
                s.append(
                    get_name_from_uri(result['s']['value']
                                      )if 's' in result else search)
                p.append("a")
                o.append(
                    get_name_from_uri(result['o']['value']
                                      ) if 'o' in result else search)

    df = pd.DataFrame({'s': s, 'p': p, 'o': o})
    return df

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
                
                select distinct ?s ?p ?o
                where {{
                    {{
                        pf:{search}
                        ?p
                        ?o .
                        bind(pf:{search} as ?s)
                    }}
                    union
                    {{
                        ?s
                        ?p
                        pf:{search} .
                        bind(pf:{search} as ?o)
                    }} 
                    union
                    {{
                        "{search}"
                        ?p
                        ?o .
                        bind("{search}" as ?s)
                    }}
                    union
                    {{
                        ?s
                        ?p
                        "{search}" .
                        bind("{search}" as ?o)
                    }}
                    FILTER NOT EXISTS
                    {{
                        ?s a  pf:{search} .
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
    return df.drop_duplicates()


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

def initclassPrefixDic():
    results = send_query("""
    prefix rdfs: <http://www.w3.org/2000/01/rdf-schema#>
    prefix owl: <http://www.w3.org/2002/07/owl#>

    SELECT ?wanted 
    WHERE {
       ?wanted a owl:Class .
    }
    """)

    dc =dict()
    for s in results["results"]["bindings"]:
        dc[get_name_from_uri(s['wanted']['value'])] = get_prefix_from_uri(s['wanted']['value'])
    return dc
    
#Allows to get a list with all the occurencies in the DB
#For the moment s, p ans o in the same list and doing that only once
def initAutocompleteList():
    
    classPrefixDic = initclassPrefixDic()
    l = list(classPrefixDic.keys())
    return l
