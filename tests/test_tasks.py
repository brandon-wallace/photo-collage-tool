from os import environ
from pathlib import Path
import pytest
from PIL import Image
from application.tasks import rename_image, save_path, resize_image


@pytest.fixture(scope='session')
def temp_file(tmpdir_factory):
    '''Create a temporary image file'''

    temp_image_obj = Image.new('RGB', size=(800, 600), color=(255, 0, 0))
    temp_directory = tmpdir_factory.mktemp('temp_dir')
    i = temp_image_obj.save(f'{temp_directory}{temp_image_obj}.jpg')
    return i


def test_rename_image():

    assert rename_image('text', 'image') == 'text_image'


def test_save_path():

    assert Path(environ.get('UPLOADED_IMAGES_DEST')) == save_path()


def test_resize_image(temp_file):

    image = resize_image(temp_file, size=500, border=10, background='black')
    assert image.mode == 'RGBA'
