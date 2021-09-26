# -*- coding: utf-8 -*-

from waitress import serve
from paste.translogger import TransLogger
from flask_cors import CORS

from api import create_app

app = create_app()
CORS(app)

if __name__ == "__main__":
    serve(TransLogger(app, setup_console_handler=False))
