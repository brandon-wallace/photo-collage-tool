'''
application/tasks.py

Tasks to resize and merge images.

'''

from os import environ
from pathlib import Path
from datetime import datetime as dt
from PIL import Image, ImageOps
from application import celery


def save_path():
    '''Set directory to save images to'''

    return Path(environ.get('UPLOADED_IMAGES_DEST'))


def resize_image(images, size=500, border=0, background=(0, 0, 0, 0)):
    '''Resize images to square shapes'''

    upload_directory = save_path()
    resized_images = []
    for img in images:
        image_obj = Image.open(f'{upload_directory}/{img}')
        image_png = image_obj.convert('RGBA')
        image_resized = image_png.resize((size, size))
        image_with_border = ImageOps.expand(image_resized, border=border,
                                            fill=background)
        filename = f'resized_{dt.utcnow().strftime("%Y%m%d-%H%M%S.%f")}.png'
        image_with_border.save(f'{upload_directory}/{filename}')
        resized_images.append(f'{filename}')
    return resized_images


@celery.task(bind=True)
def merge_images(self, image_list, filename, orientation='horizontal'):
    '''Merge images together'''

    upload_directory = save_path()
    image_objects = []
    for image_file in image_list:
        img_obj = Image.open(f'{upload_directory}/{image_file}')
        image_objects.append(img_obj)
    if orientation == 'horizontal':
        total_width = sum(img.width for img in image_objects)
        merged_image = Image.new('RGBA', (total_width,
                                 image_objects[0].height))
        x_axis = 0
        for img in image_objects:
            merged_image.paste(img, (x_axis, 0))
            x_axis += img.width
    else:
        total_height = sum(img.height for img in image_objects)
        merged_image = Image.new('RGBA', (image_objects[0].width,
                                 total_height))
        y_axis = 0
        for img in image_objects:
            merged_image.paste(img, (0, y_axis))
            y_axis += img.height
    merged_image.save(f'{upload_directory}/{filename}')
    return
