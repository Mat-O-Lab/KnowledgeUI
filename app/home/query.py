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
            select ?p ?o
            where {{
                mseo:{nameOfExperiment}
                ?p
                ?o
            }}
        """
    results = sparql.setQuery(q1)
    sparql.setReturnFormat(JSON)
    results = sparql.query().convert()
    data = []
    for result in results["results"]["bindings"]:
        data.append({'predicate':result['p']['value'],'object':result['o']['value']})
    return data

print(input_emodul_data_for_calibration('BA Los M V-4'))