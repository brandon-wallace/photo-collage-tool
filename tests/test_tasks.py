from pathlib import Path
from application.tasks import rename_image, save_image_to, resize_image


def test_rename_image():

    assert rename_image('text', 'image') == 'text_image'


def test_save_image_to():

    assert str(type(save_image_to(Path()))) == "<class 'pathlib.PosixPath'>"


def test_resize_image(image, size):

    pass
