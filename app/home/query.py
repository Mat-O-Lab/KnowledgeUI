from SPARQLWrapper import SPARQLWrapper, JSON

sparql = SPARQLWrapper("http://127.0.0.1:8080/fuseki/lebedigital")

def input_emodul_data_for_calibration(nameOfExperiment):
    nameOfExperiment = 'E-modul experiment '.replace(' ','_') + nameOfExperiment.replace(' ','_').replace('.','_')
    q1 = f"""
            prefix bwmd: <https://www.materials.fraunhofer.de/ontologies/BWMD_ontology/mid#>
            prefix mseo: <https://purl.matolab.org/mseo/mid/>
            prefix cco: <http://www.ontologyrepository.com/CommonCoreOntologies/>
            prefix obo: <http://purl.obolibrary.org/obo/>
            prefix con: <https://github.com/BAMresearch/ModelCalibration/blob/Datasets/usecases/Concrete/ConcreteOntology/Concrete_Ontology_MSEO.owl#>
            select ?rawdatapath
            where {{
                {{
                    select ?info
                    where {{
                        {{
                            select ?analyseddata
                            where{{
                                {{
                                    select ?bfo
                                    where {{
                                        {{
                                            select ?rawdata
                                            where {{
                                                mseo:{nameOfExperiment}
                                                cco:has_output
                                                ?rawdata
                                            }}
                                        }}
                                        ?rawdata
                                        cco:is_input_of
                                        ?bfo
                                    }}
                                }}
                                ?bfo
                                cco:has_output
                                ?analyseddata
                            }}
                        }}
                        ?analyseddata
                        obo:RO_0010001
                        ?info
                    }}
                    
                }}
                ?info
                cco:has_URI_value
                ?rawdatapath
            }}
            limit 1
        """
    results = sparql.setQuery(q1)
    sparql.setReturnFormat(JSON)
    results = sparql.query().convert()
    processedDataPath = ''
    for result in results["results"]["bindings"]:
        if sys.platform == 'win32':
            processedDataPath = result['rawdatapath']['value']
        else:
            processedDataPath = result['rawdatapath']['value']


    
    specimenParameterNames = ['Mass', 'Diameter', 'Length']
    specimenParameters = []
    for parameter in specimenParameterNames:
        q2 = f"""
            prefix bwmd: <https://www.materials.fraunhofer.de/ontologies/BWMD_ontology/mid#>
            prefix mseo: <https://purl.matolab.org/mseo/mid/>
            prefix cco: <http://www.ontologyrepository.com/CommonCoreOntologies/>
            prefix obo: <http://purl.obolibrary.org/obo/>
            prefix con: <https://github.com/BAMresearch/ModelCalibration/blob/Datasets/usecases/Concrete/ConcreteOntology/Concrete_Ontology_MSEO.owl#>
            select ?parametervalue
            where {{
                {{
                    select ?info
                    where {{
                        {{
                            select ?parameterclass
                            where {{
                                {{
                                    select ?parameterclass
                                    where {{
                                        {{
                                            select ?measurementregion
                                            where {{
                                                {{
                                                    select ?specimen
                                                    where {{
                                                        ?specimen
                                                        cco:is_input_of
                                                        mseo:{nameOfExperiment}
                                                    }}
                                                }}
                                                ?specimen
                                                obo:BFO_0000051
                                                ?measurementregion
                                            }}
                                        }}
                                        ?measurementregion
                                        obo:RO_0000086
                                        ?parameterclass
                                    }}
                                }}
                                ?parameterclass
                                a
                                cco:{parameter}
                            }}
                        }}
                        ?parameterclass
                        obo:RO_0010001
                        ?info
                    }}
                }}
                ?info
                cco:has_decimal_value
                ?parametervalue
            }}
            """
        results = sparql.setQuery(q2)
        for result in results["results"]["bindings"]:
            if sys.platform == 'win32':
                specimenParameters.append(result['parametervalue']['value'])
            else:
                specimenParameters.append(result['parametervalue']['value'])
    return {
        'processedDataPath': processedDataPath,
        'specimenMass': specimenParameters[0],
        'specimenDiameter': specimenParameters[1],
        'specimenLength': specimenParameters[2]
    }

print(input_emodul_data_for_calibration('BA Los M V-4'))