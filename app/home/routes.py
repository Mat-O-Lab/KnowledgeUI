# -*- encoding: utf-8 -*-
"""
Copyright (c) 2019 - present AppSeed.us
"""

from app.home import blueprint
from flask import render_template, redirect, url_for, request
from flask_login import login_required, current_user
from app import login_manager
from jinja2 import TemplateNotFound
from .query import search_string, search_number
import json


@blueprint.route('/index')
@login_required
def index():

    return render_template('index.html', segment='index')


@blueprint.route('/<template>')
@login_required
def route_template(template):

    try:

        if not template.endswith('.html'):
            template += '.html'

        # Detect the current page
        segment = get_segment(request)

        # Serve the file (if exists) from app/templates/FILE.html
        realRouter = template
        template = template.replace('.html', '')
        return render_template(realRouter, segment=segment)

    except TemplateNotFound:
        return render_template('page-404.html'), 404

    except:
        return render_template('page-500.html'), 500


@blueprint.route('/search', methods=('GET', 'POST'))
@login_required
def search():
    # try:
    if request.method == 'POST' and request.form.get('search') == 'Search':
        try:
            search = float(request.form['experiment'])
            temp = search_number(search)
            columnNames = temp.columns.values
            temp = temp.to_dict('records')

        except:
            search = request.form['experiment']
            temp = search_string(search)
            columnNames = temp.columns.values
            temp = temp.to_dict('records')
    elif request.method == 'POST' and request.form.get('search') != 'Search':
        print(request.form.get('search'))
        search = ''
        temp = {}
        columnNames = []
    else:
        search = ''
        temp = {}
        columnNames = []
   
    return render_template('search.html',
                           search=search,
                           records=temp,
                           colnames=columnNames)
    # except TemplateNotFound:
    #     return render_template('page-404.html'), 404

    # except:
    #     return render_template('page-500.html'), 500


# Helper - Extract current page name from request
def get_segment(request):

    try:

        segment = request.path.split('/')[-1]

        if segment == '':
            segment = 'index'

        return segment

    except:
        return None
