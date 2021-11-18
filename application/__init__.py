# application/__init__.py

import logging
from os import environ
from flask import Flask
from flask_uploads import configure_uploads, IMAGES, UploadSet
from celery import Celery

logger = logging.getLogger(__name__)
logger.setLevel(logging.DEBUG)
file_handler = logging.FileHandler('error.log')
formatter = logging.Formatter('%(asctime)s: %(levelname)s: \
                              %(name)s: %(message)s')
file_handler.setFormatter(formatter)
logger.addHandler(file_handler)

celery = Celery('tasks', backend='rpc://', broker='pyamqp://guest@127.0.0.1')


def create_app():
    '''Flask application factory'''

    app = Flask(__name__)

    app.config['DEBUG'] = True
    app.config['SECRET_KEY'] = environ.get('SECRET_KEY')
    app.config['UPLOADED_IMAGES_DEST'] = environ.get('UPLOADED_IMAGES_DEST')
    app.config['CELERY_TASK_TRACK_STARTED'] = True
    app.config['CELERY_RESULT_PERSISTENT'] = True
    images = UploadSet('images', IMAGES)
    configure_uploads(app, images)
    celery.conf.update(app.config)

    from application.main.routes import main
    app.register_blueprint(main)

    return app
