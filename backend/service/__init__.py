from flask import Flask

from .config import Config
from service import logger

app = Flask(__name__)


def create_app():
    """App creation"""
    app.config.from_object(Config)

    from service.api.handlers import data

    api_url_prefix = "/api"
    app.register_blueprint(data.blueprint, url_prefix=api_url_prefix)

    return app
