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
from utilities import parse_sunburst, fetch_overview_data

config_name = os.environ.get("APP_MODE") or "development"

app = Flask(__name__)
CORS(app)
app.config.from_object(config[config_name])
bootstrap = Bootstrap(app)

ENDPOINT = app.config['SPARQL_ENDPOINT']
SPARKLIS_OPTIONS = app.config['SPARKLIS_OPTIONS']
app.overview_data = parse_sunburst(fetch_overview_data(ENDPOINT))

"""
Initialize global variables for jinja2 templates (e.g. allow global access to the specified SPARQL endpoint).
"""
@app.context_processor
def init_global_vars_template():
    return {"endpoint": ENDPOINT, "sparklis_options": SPARKLIS_OPTIONS}

@app.route('/', methods=['GET', 'POST'])
def index():

    #sunburst_data = parse_sunburst(res.text)

    logo = './static/resources/MatOLab-Logo.svg'
    message = ''
    result = ''
    return render_template(
        "index.html",
        logo=logo,
        message=message,
        result=result,
        sunburst_data=app.overview_data
        )

@app.route('/osparklis.html', methods=['GET'])
def explore():
    logo = './static/resources/MatOLab-Logo.svg'
    return render_template(
        "osparklis.html", 
        logo=logo
    )

@app.route('/predef.html', methods=['GET'])
def query():
    logo = './static/resources/MatOLab-Logo.svg'
    return render_template(
        "predef.html",
        logo=logo
    )

if __name__ == "__main__":
    port = int(os.environ.get("PORT", 5000))
    app.run(host="0.0.0.0", port=port, debug=app.config["DEBUG"])