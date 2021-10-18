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

    default_path = environ.get('UPLOADED_IMAGES_DEST')
    return Path(default_path)


def resize_image(image_file, size, border, background):
    '''Resize images'''

    image = Image.open(image_file)
    image_png = image.convert('RGBA')
    image_resized = image_png.resize((size, size))
    image_with_border = ImageOps.expand(image_resized,
                                        border=border, fill=background)
    filename = f'resized_{datetime.utcnow().strftime("%Y%m%d-%H%M%S%f")}.png'
    image_with_border.save(save_path / filename)
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
def generate_collage(images, size, border, background, orientation):

    all_images = []
    for image_file in images:
        resized = resize_image(image_file, size, border, background)
        all_images.append(resized)
    collage = merge_images(all_images)
    filename = f'collage_{datetime.utcnow().strftime("%Y%m%d-%H%M%S.%f")}.png'
    collage.save(save_path / filename)
