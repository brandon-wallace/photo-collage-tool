from os import environ
from pathlib import Path
import numpy
from PIL import Image
from application import celery

default_path = environ.get('UPLOADED_IMAGES_DEST')


def rename_image(label, img):
    '''Rename images'''

    return f'{label}_{img}'


def save_images_to(path):
    '''Set directory to save images to'''

    path_to_file = Path(path)
    return path_to_file


@celery.task(bind=True)
def resize_image(self, img, size):
    '''Resize images'''

    new_img = rename_image('resized', img)
    location = save_images_to(default_path)
    pic = Image.open(Path(location / img))
    pic = pic.convert('RGBA')
    resized_pic = pic.resize((size, size))
    return resized_pic.save(str(Path(location / new_img)), format='PNG')


@celery.task()
def create_thumbnail(img):
    '''Create thumbnail images'''

    new_img = rename_image('thumbnail', img)
    location = save_images_to(default_path)
    pic = Image.open(Path(location / img))
    pic = pic.convert('RGBA')
    pic.thumbnail((100, 100))
    return pic.save(Path(location / new_img), format='PNG')


@celery.task()
def merge_images(img_files, orientation='horizontal'):
    '''Merge images together'''

    images = [Image.open(img) for img in img_files]
    convert_to_png = [img.convert('RGBA') for img in images]
    resized_png = [img.resize((400, 400)) for img in convert_to_png]
    img_array = [numpy.asarray(img) for img in resized_png]
    merged_images = numpy.hstack((img_array))
    collage = Image.fromarray(merged_images)
    # images = [Image.open(img) for img in img_files]
    # img_arr = [numpy.asarray(img) for img in images]
    # img_fromarr = [numpy.fromarray(img) for img in img_arr]
    # if orientation == 'vertical':
    #     return numpy.vstack(tuple(img_fromarr))
    # return numpy.hstack(tuple(img_fromarr))
    return collage
