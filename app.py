from email import header
import os

from flask import Flask, flash, request, jsonify, render_template
from flask_wtf import FlaskForm
from flask_bootstrap import Bootstrap
from flask_cors import CORS

from rdflib import Graph
from rdflib.query import Result
import requests
import io

from config import config
from utilities import parse_sunburst

config_name = os.environ.get("APP_MODE") or "development"

app = Flask(__name__)
CORS(app)
app.config.from_object(config[config_name])
bootstrap = Bootstrap(app)

ENDPOINT = app.config['SPARQL_ENDPOINT']

"""
Initialize global variables for jinja2 templates (e.g. allow global access to the specified SPARQL endpoint).
"""
@app.context_processor
def init_global_vars_template():
    return dict(endpoint=ENDPOINT)

@app.route('/', methods=['GET', 'POST'])
def index():

    app.logger.info('querying for sunburst graph')

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

    res = requests.get(ENDPOINT, params={'query': query}, headers={'Accept': 'text/csv'})
    
    sunburst_data = parse_sunburst(res.text)

    logo = './static/resources/MatOLab-Logo.svg'
    message = ''
    result = ''
    return render_template(
        "index.html",
        logo=logo,
        message=message,
        result=result,
        sunburst_data=sunburst_data
        )

@app.route('/osparklis.html', methods=['GET'])
def explore():

    logo = './static/resources/MatOLab-Logo.svg'
    message = ''
    result = ''

    return render_template(
        "osparklis.html",
        logo=logo,
        message=message,
        result=result,
    )

if __name__ == "__main__":
    port = int(os.environ.get("PORT", 5000))
    app.run(host="0.0.0.0", port=port, debug=app.config["DEBUG"])
