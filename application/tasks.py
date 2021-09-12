from os import environ
from pathlib import Path
from datetime import datetime
import numpy
from PIL import Image, ImageOps
from application import celery

default_path = environ.get('UPLOADED_IMAGES_DEST')


def rename_image(label, image):
    '''Rename images'''

    return f'{label}_{image}'


def save_image_to(path):
    '''Set directory to save images to'''

    return Path(path)


def resize_image(image, size):
    '''Resize images'''

    return image.resize((size, size))


def merge_images(image_file, border, background=(0, 0, 0, 0)):

    image_path = save_image_to(default_path)

    image = Image.open(Path(image_path / image_file))
    image_png = image.convert('RGBA')
    image_resized = resize_image(image_png, 500)
    image_expanded_border = ImageOps.expand(image_resized, border=int(border),
                                            fill=background)
    image_array = numpy.asarray(image_expanded_border)
    return image_array


@celery.task()
def generate_collage(images, orientation):

    save_path = save_image_to(default_path)

    image_array = [img for img in images]
    if orientation == 'vertical':
        merged_images = numpy.vstack((image_array))
    else:
        merged_images = numpy.hstack((image_array))
    collage = Image.fromarray(merged_images)
    filename = f'collage_{datetime.utcnow().strftime("%Y%m%d%H%M%S")}.png'
    collage.save(Path(save_path / filename))
    return filename
