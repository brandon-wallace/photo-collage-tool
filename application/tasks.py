from pathlib import Path
# from flask import current_app
from application import celery
from PIL import Image


# @celery.task
def resize_image(img, size):
    '''Resize images'''

    new_img = f'renamed_{img}'
    location = Path('uploads/images')
    pic = Image.open(Path(location / img))
    print(pic.filename)
    pic = pic.convert('RGBA')
    resized_picture = pic.resize((size, size))
    return resized_picture.save(Path(location / new_img), format='PNG')
