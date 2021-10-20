# application/tasks.py

from os import environ
from pathlib import Path
from datetime import datetime
from PIL import Image, ImageOps
from application import celery


def rename_image(label, image):
    '''Rename images'''

    return f'{label}_{image}'


def save_path():
    '''Set directory to save images to'''

    return Path(environ.get('UPLOADED_IMAGES_DEST'))


@celery.task
def resize_image(images, size, border, background):
    '''Resize images to square shapes'''

    upload_directory = save_path()
    resized_images = []
    for img in images:
        image = Image.open(f'{upload_directory}/{img}')
        image_png = image.convert('RGBA')
        image_resized = image_png.resize((size, size))
        image_with_border = ImageOps.expand(image_resized, border=border,
                                            fill=background)
        filename = f'resized_{datetime.utcnow().strftime("%Y%m%d-%H%M%S%f")}'
        image_with_border.save(f'{upload_directory}/{filename}.png')
        image_png_new = Image.open(f'{upload_directory}/{filename}.png')
        resized_images.append(image_png_new.filename)
    return resized_images


@celery.task()
def merge_images(image_list):
    '''Merge images together'''

    image_objects = []
    for filename in image_list:
        img_obj = Image.open(save_path() / filename)
        image_objects.append(img_obj)
    total_width = sum(img.width for img in image_objects)
    merged_image = Image.new('RGBA', (total_width, image_objects[0].height))
    x_axis = 0
    for img in image_objects:
        merged_image.paste(img, (x_axis, 0))
        x_axis += img.width
    filename = f'collage_{datetime.utcnow().strftime("%Y%m%d-%H%M%S.%f")}.png'
    merged_image.save(save_path() / filename)
    return filename
