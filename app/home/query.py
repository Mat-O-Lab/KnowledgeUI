from SPARQLWrapper import SPARQLWrapper, JSON
from xml.dom.minidom import NamedNodeMap
import rdflib
from SPARQLWrapper import SPARQLWrapper
import os
from decouple import config
from pathlib import Path
import sys
import pandas as pd
from app.home import classPrefixDic

baseDir0 = Path(__file__).resolve().parents[0]
baseDir1 = Path(__file__).resolve().parents[1]
baseDir2 = Path(__file__).resolve().parents[2]

if sys.platform == 'win32':
    prefixPath = 'file:///' + os.path.join(baseDir1, 'data').replace(
        '\\', '/') + '/'
else:
    prefixPath = 'file://' + os.path.join(baseDir1, 'data') + '/'

# Global that connects to the dataset. 
# To change the link to the dataset change it in the file .env
sparql = SPARQLWrapper(config('DATASET_LINK'))

# We will get rid of those prefixes when all the query functions will be
# compatible with the global variable classPrefixDic in __init__.py
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
    """
    Takes an uri and returns a string containing the name at the end of the uri

    Arguments:
    uri -> a string

    Returns:
    name -> a string
    
    Example: get_name_from_uri("http://www.w3.org/2002/07/owl#type") returns type
    """

    i = uri.rfind('/') + 1
    k = uri.rfind('#') + 1

    name = uri[i:] if k < i else uri[k:]
    return name

def get_prefix_from_uri(uri):
    """
    Takes an uri and returns it's prefix

    Arguments:
    uri -> a string

    Returns:
    name -> a string
    
    Example: get_name_from_uri("http://www.w3.org/2002/07/owl#type") 
    returns http://www.w3.org/2002/07/owl#
    """

    i = uri.rfind('/') + 1
    k = uri.rfind('#') + 1

    pf = uri[:i] if k < i else uri[:k]
    return pf

def send_query(q1):
    """Send a SPARQL query to the database and return the result
    
    Arguments:
    q1 -> string containing query
    
    Returns:
    Result of the query -> dict[]
    """
    sparql.setQuery(q1)
    sparql.setReturnFormat(JSON)
    return sparql.query().convert()

def search_instances(search):
    """
    Search for instances from a given class and return the in dataframe.
    
    Arguments:
    search -> string representing a class name

    Returns:
    df -> a dataframe of the following shape

    s    |    p     |      o
    ---------------------------------
    S1   |    P1    |      O1
    ---------------------------------
    S2   |    P1    |      O2        
    ---------------------------------
    .    |     .    |      .         
    ---------------------------------
    .    |     .    |      .         
    ---------------------------------
    .    |     .    |      .         
    """
    try:
        search = search.replace(' ', '_').replace('.', '_')
    except:
        search = search

    s = []
    p = []
    o = []

    pref = classPrefixDic[search] if search in classPrefixDic else ""
    q1 = f"""
            prefix pf:<{pref}>
            
            select ?s ?p ?o
            where {{
                {{
                    ?s
                    a
                    pf:{search}
                }} 
            }}
        """
    if pref == "":
        q1 = f"""
        select ?s ?p ?o
        where {{
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
    """
    Search all triplets related to a given class except it's instances.
   
    Arguments:
    search -> string representing a class name

    Returns:
    df -> a dataframe of the following shape

    s    |    p     |      o
    ---------------------------------
    S1   |    P1    |      O1
    ---------------------------------
    S2   |    P1    |      O2        
    ---------------------------------
    .    |     .    |      .         
    ---------------------------------
    .    |     .    |      .         
    ---------------------------------
    .    |     .    |      .  
    """
    try:
        search = search.replace(' ', '_').replace('.', '_')
    except:
        search = search
    
    s = []
    p = []
    o = []

    pref = classPrefixDic[search] if search in classPrefixDic else ""
    
    q1 = f"""
            prefix pf: <{pref}>
            
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
                FILTER NOT EXISTS
                {{
                    ?s a  pf:{search} .
                }}
            }}
        """
    if pref == "":
        q1 = f"""
            select distinct ?s ?p ?o
            where {{
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
                    ?s a  "{search}" .
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
    """
    Search for all triplets containing a givent numeric value
    
    Arguments:
    search -> float

    Returns:
    df -> a dataframe of the following shape

    s    |    p     |      o
    ---------------------------------
    S1   |    P1    |      O1
    ---------------------------------
    S2   |    P1    |      O2        
    ---------------------------------
    .    |     .    |      .         
    ---------------------------------
    .    |     .    |      .         
    ---------------------------------
    .    |     .    |      .  
    """

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
    """This is used when we do a search by clicking on link
    
    Arguments:
    search -> string representing a class name

    Returns:
    df -> a dataframe of the following shape

    s    |    p     |      o
    ---------------------------------
    S1   |    P1    |      O1
    ---------------------------------
    S2   |    P1    |      O2        
    ---------------------------------
    .    |     .    |      .         
    ---------------------------------
    .    |     .    |      .         
    ---------------------------------
    .    |     .    |      .  
    """
    try:
        search = search.replace(' ', '_').replace('.', '_')
    except:
        search = search

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