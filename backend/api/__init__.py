from flask import Flask

from .config import Config
from api import logger

app = Flask(__name__, template_folder="../web/templates")


def create_app():
    """App creation"""
    app.config.from_object(Config)

    from api.api.handlers import data

    api_url_prefix = "/api"
    app.register_blueprint(data.blueprint, url_prefix=api_url_prefix)

    from web.views import users

    app.register_blueprint(users.blueprint)

    return app
