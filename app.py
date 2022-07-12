import os

from flask import Flask, flash, request, jsonify, render_template
from flask_wtf import FlaskForm
from flask_bootstrap import Bootstrap
from flask_cors import CORS

from rdflib import Graph

from config import config

config_name = os.environ.get("APP_MODE") or "development"

app = Flask(__name__)
CORS(app)
app.config.from_object(config[config_name])
bootstrap = Bootstrap(app)

"""
Initialize global variables for jinja2 templates (e.g. allow global access to the specified SPARQL endpoint).
"""
@app.context_processor
def init_global_vars_template():
    return dict(endpoint=app.config['SPARQL_ENDPOINT'])

@app.route('/', methods=['GET', 'POST'])
def index():
    logo = './static/resources/MatOLab-Logo.svg'
    message = ''
    result = ''
    return render_template(
        "index.html",
        logo=logo,
        message=message,
        result=result
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
