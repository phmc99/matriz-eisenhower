from flask import Flask
from app.routes.blueprints import bp_api


def init_app(app: Flask):
    app.register_blueprint(bp_api)
