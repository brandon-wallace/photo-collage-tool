# application/tasks.py

from os import environ
from pathlib import Path
from datetime import datetime
from PIL import Image, ImageOps
from application import celery


def save_path():
    '''Set directory to save images to'''

    return Path(environ.get('UPLOADED_IMAGES_DEST'))


# @celery.task
def resize_image(images, size, border, background=(0, 0, 0, 0)):
    '''Resize images to square shapes'''

    upload_directory = save_path()
    resized_images = []
    for img in images:
        image_obj = Image.open(f'{upload_directory}/{img}')
        image_png = image_obj.convert('RGBA')
        image_resized = image_png.resize((size, size))
        image_with_border = ImageOps.expand(image_resized, border=border,
                                            fill=(0, 0, 0, 0))
        filename = f'resized_{datetime.utcnow().strftime("%Y%m%d-%H%M%S%f")}'
        image_with_border.save(f'{upload_directory}/{filename}.png')
        resized_images.append(f'{filename}.png')
    return {'resized_images': resized_images}


@celery.task
def merge_images(image_list, orientation='horizontal'):
    '''Merge images together'''

    upload_directory = save_path()
    image_objects = []
    for filename in image_list:
        img_obj = Image.open(f'{upload_directory}/{filename}')
        image_objects.append(img_obj)
    if orientation == 'horizontal':
        total_width = sum(img.width for img in image_objects)
        merged_image = Image.new('RGBA', (total_width, image_objects[0].height))
        x_axis = 0
        for img in image_objects:
            merged_image.paste(img, (x_axis, 0))
            x_axis += img.width
    else:
        total_height = sum(img.height for img in image_objects)
        merged_image = Image.new('RGBA', (image_objects[0].width, total_height))
        y_axis = 0
        for img in image_objects:
            merged_image.paste(img, (0, y_axis))
            y_axis += img.height
    filename = f'collage_{datetime.utcnow().strftime("%Y%m%d-%H%M%S.%f")}.png'
    merged_image.save(f'{upload_directory}/{filename}')
    return {'filename': filename}
