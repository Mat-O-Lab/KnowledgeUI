function redirect_to_osparklis() {
    var a = document.getElementById('sparklis-custom');
    var url = window.location.search;
    const urlParams = new URL(window.location.protocol + "//" + window.location.host + "/osparklis.html" + url)
    const sparqlEndpointInput = ""
    var endpointValue = ""
    var defaultEndpoint = document.getElementById("sparql-endpoint-val").value
    var userDefinedEndpoint = document.getElementById("sparql-endpoint-input").value
    if (url != ""){
        endpointValue = url.split('=')[1]
    } else if (userDefinedEndpoint != null && userDefinedEndpoint != ""){
        endpointValue = userDefinedEndpoint
    } else {
        endpointValue = defaultEndpoint
    }

    urlParams.searchParams.append('endpoint', endpointValue);
    //todo get endpoint_value from the proper url param
    urlParams.searchParams.append('sparklis-query', endpointValue);
    urlParams.searchParams.append('sparklis-path','D');
    urlParams.searchParams.append('entity_lexicon_select','http://www.w3.org/2000/01/rdf-schema#label');
    urlParams.searchParams.append('concept_lexicons_select','http://www.w3.org/2000/01/rdf-schema#label');
    urlParams.searchParams.append('concept_tooltips_select','http://www.w3.org/2000/01/rdf-schema#label');


//    var query_url = new URL(window.location.protocol + "//" + window.location.host + "/osparklis.html");
//    winAddress = query_url.toString() + '&sparklis-query=%5BVId%5DReturn%28Det%28An%281%2CModif%28Select%2CUnordered%29%2CClass%28%22%22%29%29%2CNone%29%29'
    window.open(urlParams,"_self");
}


