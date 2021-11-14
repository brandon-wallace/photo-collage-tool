'''
tests/test_tasks.py
'''

from os import environ
from pathlib import Path
from application.tasks import save_path


def test_save_path():
    '''Test path where files are saved'''

    assert Path(environ.get('UPLOADED_IMAGES_DEST')) == save_path()
