import os

from flask import Flask, json


def create_app():
    app = Flask(__name__)
	app.config['DEBUG'] = os.environ.get('APP_DEBUG', False)

	from .api import bp as api_blueprint
	app.register_blueprint(api_blueprint)

	return app
