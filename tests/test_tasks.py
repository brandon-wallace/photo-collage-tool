from pathlib import Path
from application.tasks import rename_image, save_image_to


def test_rename_image():

    assert rename_image('text', 'image') == 'text_image'


def test_save_image_to():

    assert save_image_to('/') == Path('/')
