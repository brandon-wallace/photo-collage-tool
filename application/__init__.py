# application/__init__.py

import logging
from os import environ
from flask import Flask
from flask_uploads import configure_uploads, IMAGES, UploadSet

logger = logging.getLogger(__name__)
logger.setLevel(logging.DEBUG)
file_handler = logging.FileHandler('error.log')
formatter = logging.Formatter('%(asctime)s: %(levelname)s: \
                              %(name)s: %(message)s')
file_handler.setFormatter(formatter)
logger.addHandler(file_handler)


def create_app():
    '''Flask application factory'''

    app = Flask(__name__)

    app.config['DEBUG'] = True
    app.config['SECRET_KEY'] = environ.get('SECRET_KEY')
    app.config['UPLOADED_IMAGES_DEST'] = 'uploads/images'
    images = UploadSet('images', IMAGES)
    configure_uploads(app, images)

    from application.main.routes import main
    app.register_blueprint(main)

    return app
