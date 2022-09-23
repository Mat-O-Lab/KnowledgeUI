from email import header
import os
<<<<<<< HEAD
import io
=======
import pandas as pd
import numpy as np
from material_discovery import *

import matplotlib

matplotlib.use('Agg')
import matplotlib.pyplot as plt
from io import BytesIO
>>>>>>> origin/main

from flask import Flask, flash, request, jsonify, render_template, redirect, url_for
from flask_wtf import FlaskForm
from flask_bootstrap import Bootstrap
from flask_cors import CORS
import pandas as df

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
dataset = pd.read_csv('static/resources/MaterialsDiscoveryExampleData.csv')

@app.context_processor
def init_global_vars_template():
    """ Initialize global variables for jinja2 templates (e.g. allow global access to the specified SPARQL endpoint).
    """
    return dict(endpoint=ENDPOINT,
                sparklis_options=SPARKLIS_OPTIONS,
                logo='./static/resources/MatOLab-Logo.svg'
                )


@app.route('/', methods=['GET', 'POST'])
def index():
    """ This is the main function which redirects here after lunching

    It allows both post and get methods and initializes some general parameters
    like logo and message once called

    Parameters
    ----------

    """
    # sunburst_data = parse_sunburst(res.text)
    message = ''
    result = ''
    return render_template(
        "index.html",
        message=message,
        result=result,
        sunburst_data=app.overview_data
    )


@app.route('/osparklis.html', methods=['GET'])
def explore():
    """ Display Sparklis Web Application for /osparklis.html route.      
    """
    return render_template("osparklis.html")


@app.route('/predef.html', methods=['GET'])
def query():
    return render_template("predef.html")


@app.route('/predict', methods=['POST', 'GET'])
def model_process():
    model = request.form.get('models')
    target_df = request.form.getlist('targets')
    feature_df = request.form.getlist('feature_df')
    fixed_target_df = request.form.getlist('fixedtargets')
    strategy = request.form.get('strategies')
    # distance = request.form.get('initial_sample')
    sigma = request.form.get('sigma_factor')


    # dataframe = loadDataset(dataset)
    dataframe = pd.read_csv('static/resources/MaterialsDiscoveryExampleData.csv')
    columns = dataframe.columns
    # --- This is the min_max of benchmarking ---------
    min_or_max_target = {}
    for t in target_df:
        x = 'Rd_' + t
        min_or_max_target[t] = request.form.get(x)

    target_selected_number2 = {}
    for t in target_df:
        x = 'Nd_' + t
        target_selected_number2[t] = int(request.form.get(x))
    # ---------------------------------
    min_or_max_fixedtarget = {}
    for t in fixed_target_df:
        x = 'Rd1_' + t
        min_or_max_fixedtarget[t] = request.form.get(x)

    fixedtarget_selected_number2 = {}
    for t in fixed_target_df:
        x = 'Nd1_' + t
        fixedtarget_selected_number2[t] = int(request.form.get(x))
    return render_template('predict.html')
    # ------------------------------------------------
    """ 
    #Just remove the comment and run the model:
    l = learn(dataframe, model,  target_df, feature_df, fixed_target_df, strategy, sigma, target_selected_number2,
              fixedtarget_selected_number2, min_or_max_target, min_or_max_fixedtarget)
    l.start_learning()
    n = l.start_learning()

    df_table = pd.DataFrame(n)
    df_column = df_table.columns
    # df_table2 = df_table1[1:]
    print(df_column)
    df_only_data = df_table

    return render_template('predict.html', columns=columns, df_column=df_column, df_only_data=df_only_data,
                           n=n.to_html(index=False, classes='table table-striped table-hover table-responsive',
                                       escape=False))
    """

def parse_json_object_to_df(json_data):
    csv_rows = [','.join(json_data.columns)] + [','.join(row) for row in json_data.columns]
    dataframe = df.read_csv(io.StringIO('\n'.join(csv_rows)))
    return dataframe

if __name__ == "__main__":
    port = int(os.environ.get("PORT", 5000))
    app.run(host="0.0.0.0", port=port, debug=app.config["DEBUG"])
