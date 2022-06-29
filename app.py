import os

from flask import Flask, flash, request, jsonify, render_template
from flask_wtf import FlaskForm
from flask_bootstrap import Bootstrap

from config import config

config_name = os.environ.get("APP_MODE") or "development"

app = Flask(__name__)
app.config.from_object(config[config_name])
bootstrap = Bootstrap(app)

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

if __name__ == "__main__":
    port = int(os.environ.get("PORT", 5000))
    app.run(host="0.0.0.0", port=port, debug=app.config["DEBUG"])
