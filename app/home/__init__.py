# -*- encoding: utf-8 -*-
"""
Copyright (c) 2019 - present AppSeed.us
"""

from flask import Blueprint
from SPARQLWrapper import SPARQLWrapper, JSON
import json
from decouple import config

def get_name_from_uri_init(uri):
    i = uri.rfind('/') + 1
    k = uri.rfind('#') + 1

    name = uri[i:] if k < i else uri[k:]
    return name

def get_prefix_from_uri_init(uri):
    i = uri.rfind('/') + 1
    k = uri.rfind('#') + 1

    pf = uri[:i] if k < i else uri[:k]
    return pf

def initclassPrefixDic():
    sparql = SPARQLWrapper(config('DATASET_LINK'))

    sparql.setQuery("""
    prefix rdfs: <http://www.w3.org/2000/01/rdf-schema#>
    prefix owl: <http://www.w3.org/2002/07/owl#>

    SELECT ?wanted 
    WHERE {
       ?wanted a owl:Class .
    }
    """)
    sparql.setReturnFormat(JSON)
    results = sparql.query().convert()

    dc =dict()
    for s in results["results"]["bindings"]:
        dc[get_name_from_uri_init(s['wanted']['value'])] = get_prefix_from_uri_init(s['wanted']['value'])
    return dc
    
#Allows to get a list with all the occurencies in the DB
#For the moment s, p ans o in the same list and doing that only once
def initAutocompleteList():
    
    classPrefixDic = initclassPrefixDic()
    l = list(classPrefixDic.keys())
    return l, classPrefixDic

blueprint = Blueprint(
    'home_blueprint',
    __name__,
    url_prefix='',
    template_folder='templates',
    static_folder='static'
)

autoCompList, classPrefixDic = initAutocompleteList()