import os

from flask import Flask, flash, request, jsonify, render_template
from flask_wtf import FlaskForm
from flask_bootstrap import Bootstrap
from flask_cors import CORS
from config import config

config_name = os.environ.get("APP_MODE") or "development"

app = Flask(__name__)
CORS(app)
app.config.from_object(config[config_name])
bootstrap = Bootstrap(app)

@app.route('/', methods=['GET', 'POST'])
def index():
    """ This is the main function which redirects here after lunching

    It allows both post and get methods and initializes some general parameters
    like logo and message once called

    Parameters
    ----------

    """

    logo = './static/resources/MatOLab-Logo.svg'
    message = ''
    result = ''
    return render_template(
        "index.html",
        logo=logo,
        message=message,
        result=result
        )

# TODO: add logo, message and result to a general function instead of defining in every function separately

@app.route('/osparklis.html', methods=['GET'])
def explore():
    """ render explore tab in the main page
    it only allows get methods

    Parameters
    
    
    """
    
    logo = './static/resources/MatOLab-Logo.svg'
    return render_template(
        "osparklis.html",
        logo=logo
    )

if __name__ == "__main__":
    port = int(os.environ.get("PORT", 5000))
    app.run(host="0.0.0.0", port=port, debug=app.config["DEBUG"])
