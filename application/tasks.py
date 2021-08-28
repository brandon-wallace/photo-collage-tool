from os import environ
from pathlib import Path
# from flask import current_app
from application import celery
from PIL import Image
from time import sleep

default_path = environ.get('UPLOADED_IMAGES_DEST')


# @celery.task
def rename_image(label, img):
    '''Rename images'''

    return f'{label}_{img}'


# @celery.task
def save_images_to(path):
    '''Set directory to save images to'''

    path_to_file = Path(path)
    return path_to_file


@celery.task
def resize_image(img, size):
    '''Resize images'''

    new_img = rename_image('resized', img)
    location = save_images_to(default_path)
    pic = Image.open(Path(location / img))
    pic = pic.convert('RGBA')
    resized_picture = pic.resize((size, size))
    return resized_picture.save(str(Path(location / new_img)), format='PNG')


@celery.task
def create_thumbnail(img, size):
    '''Create thumbnail images'''

    new_img = rename_image('thumbnail', img)
    location = save_images_to(default_path)
    pic = Image.open(Path(location / img))
    pic = pic.convert('RGBA')
    thumbnail_image = pic.thumbnail()
    return thumbnail_image.save(Path(location / new_img), format='PNG')
