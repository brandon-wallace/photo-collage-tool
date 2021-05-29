# application/__init__.py

import logging
from os import environ
from flask import Flask

logger = logging.getLogger(__name__)
logger.setLevel(logging.DEBUG)
file_handler = logging.FileHandler('application_error.log')
formatter = logging.Formatter('%(asctime)s: %(levelname)s: \
                              %(name)s: %(message)s')
file_handler.setFormatter(formatter)
logger.addHandler(file_handler)


def create_app():
    '''Flask application factory'''

    app = Flask(__name__)

    app.config['DEBUG'] = True
    app.config['SECRET_KEY'] = environ.get('SECRET_KEY')

    from application.main.routes import main
    app.register_blueprint(main)

    return app
