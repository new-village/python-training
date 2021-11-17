""" app.py
"""
import json

import requests
from flask import Flask, Blueprint


def launch_app():
    app = Flask(__name__)
    app.config["JSON_AS_ASCII"] = False

    # Load Views
    from views import blueprints
    for bp in blueprints:
        app.register_blueprint(bp)

    return app


app = launch_app()
api = Blueprint("api", __name__, url_prefix="/estate")


if __name__ == '__main__':
    app.run(debug=True)
