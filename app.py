from email import header
import os
import re
import pandas as pd
import numpy as np
from material_discovery import *

import matplotlib

matplotlib.use('Agg')
import matplotlib.pyplot as plt
from io import BytesIO

from flask import Flask, flash, request, jsonify, render_template, redirect, url_for
from flask_wtf import FlaskForm
from flask_bootstrap import Bootstrap5
from flask_cors import CORS
import pandas as df
from requests import HTTPError
import requests

from config import config
from utilities import parse_sunburst, fetch_overview_data, parse_json_string_to_df

config_name = os.environ.get("APP_MODE") or "development"

app = Flask(__name__)
CORS(app)
app.config.from_object(config[config_name])
bootstrap = Bootstrap5(app)

ENDPOINT = app.config['SPARQL_ENDPOINT']
SPARKLIS_OPTIONS = app.config['SPARKLIS_OPTIONS']
# try:
#     app.overview_data = parse_sunburst(fetch_overview_data(ENDPOINT))
# except HTTPError as h:
#      app.overview_data = str(h)
app.overview_data = None
app.error_occured = False
app.error_message = None
user_endpoint = None
#  fetch_dataset function enhances the ability of calling
#  fuseki database to fetch the data during the run time
def fetch_data_from_endpoint(endpoint) :
    try:
        app.overview_data = parse_sunburst(fetch_overview_data(endpoint))
        app.error_occured = False
    except Exception as e:
        app.error_occured = True
        app.error_message = list(e.args) + [type(e)]
    return app.overview_data

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
    """ This is the main function which redirects here after launching
    It allows both post and get methods and initializes some general parameters
    like logo and message once called
    Parameters
    ----------
    """
    # sunburst_data = parse_sunburst(res.text)
    user_endpoint = request.values.get('sparql-endpoint-input')
    if (user_endpoint == None):
        user_endpoint = ENDPOINT
    message = ''
    result = ''

    sunburst_data_from_endpoint = fetch_data_from_endpoint(user_endpoint)
    # check if the error flag is true and then render the error template
    if (app.error_occured == True):
        return render_template(
           "error.html",
            message=message,
            result=result,
            error_message=app.error_message
            # message=app.
        )
    else:
        return render_template(
            "index.html",
            message=message,
            result=result,
            sunburst_data=sunburst_data_from_endpoint,
            endpoint=user_endpoint
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
    dataframe=pd.DataFrame()
    if dataframe.empty and "results" in request.values.keys():
        results = request.values.get('results')
        dataframe = parse_json_string_to_df(results)

    else:
        dataframe = df.read_csv('static/resources/AluTrace_Web4Genmet-CO2_result_extra.csv')
        #dataframe = df.read_csv('static/resources/MaterialsDiscoveryExampleData.csv')
    columns = dataframe.columns
    form=request.form
    
    #print(request.method)
    #print(dataframe)
    print(form)
    # if not dataframe.empty:
    #     flash('No input data given')
    #     return render_template('predict.html', columns=columns, form=form)
    

    
    if request.method == 'POST':
        model = request.form.get('models')
        target_df = request.form.getlist('targets')
        feature_df = request.form.getlist('features')
        fixed_target_df = request.form.getlist('fixedtargets')
        strategy = request.form.get('strategies')
        # distance = request.form.get('initial_sample')
        sigma = request.form.get('sigma_factor')
        print(feature_df)
        #print(target_df)
        # --- This is the min_max of benchmarking ---------
        min_or_max_target = {}
        for t in target_df:
            x = 'R_'+t
            min_or_max_target[t]= request.form.get(x)


        check_to_use_threshold_t = {}
        for t in target_df:
            x = 'C_'+t
            check_to_use_threshold_t[t]= request.form.get(x)


        target_selected_number1 = {}
        for t in target_df:
            x = 'N1_'+t
            target_selected_number1[t]= request.form.get(x)

        target_selected_number2 = {}
        for t in target_df:
            x = 'N2_'+t
            target_selected_number2[t]= request.form.get(x)

        min_or_max_fixedtarget = {}
        for t in fixed_target_df:
            x = 'R1_'+t
            min_or_max_fixedtarget[t]= request.form.get(x)


        check_to_use_threshold_ft = {}
        for t in fixed_target_df:
            x = 'C1_'+t
            check_to_use_threshold_ft[t]= request.form.get(x)


        fixedtarget_selected_number1 = {}
        for t in fixed_target_df:
            x = 'N11_'+t
            fixedtarget_selected_number1[t]= request.form.get(x)

        fixedtarget_selected_number2 = {}
        for t in fixed_target_df:
            x = 'N22_'+t
            fixedtarget_selected_number2[t]= request.form.get(x)
        
        l = learn(dataframe, model,  target_df, feature_df, fixed_target_df, strategy, sigma, target_selected_number2,
                  fixedtarget_selected_number2, min_or_max_target, min_or_max_fixedtarget)
        l.start_learning()
        n = l.start_learning()
        df_table = pd.DataFrame(n)
        df_column = df_table.columns
        # df_table2 = df_table1[1:]
        #print(df_column)
        df_only_data = df_table

        return render_template('score.html', columns=columns, df_column=df_column, df_only_data=df_only_data,  dataframe=dataframe,
                            n=n.to_html(index=False, classes='table table-striped table-hover table-responsive',
                                        escape=False))
    else:
        return render_template('predict.html', columns=columns, dataframe=dataframe, form=form)


if __name__ == "__main__":
    port = int(os.environ.get("PORT", 5000))
    app.run(host="0.0.0.0", port=port, debug=app.config["DEBUG"])