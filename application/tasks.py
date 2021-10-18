# application/tasks.py

from os import environ
from pathlib import Path
from datetime import datetime
from PIL import Image, ImageOps
from application import celery

default_path = environ.get('UPLOADED_IMAGES_DEST')


def rename_image(label, image):
    '''Rename images'''

    return f'{label}_{image}'


def save_image_to(path):
    '''Set directory to save images to'''

    return Path(path)


def resize_image(image_file, size, border, background):
    '''Resize images'''

    image = Image.open(image_file)
    image_png = image.convert('RGBA')
    image_resized = image_png.resize((size, size))
    image_with_border = ImageOps.expand(image_resized,
                                        border=border, fill=background)
    filename = f'resized_{datetime.utcnow().strftime("%Y%m%d-%H%M%S%f")}.png'
    image_with_border.save(filename)
    return image_with_border


def merge_images(image_list):

    total_width = sum(img.width for img in image_list)
    merged_image = Image.new('RGB', (total_width, image_list[0].height))
    x_axis = 0
    for img in image_list:
        merged_image.paste(img, (x_axis, 0))
        x_axis += img.width
    return merged_image


@celery.task()
def generate_collage(images, orientation):

    pass
