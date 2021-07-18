# import time
from pathlib import Path
from flask import current_app
from application import celery
from PIL import Image


@celery.task
def resize_image(img, size):
    '''Resize images'''

    location = Path('uploads/images')
    pic = Image.open(str(Path(location / img)))
    print(pic)
    resized_picture = pic.resize((size, size))
    return resized_picture.save(Path(location / 'pic_resized.jpg'))
#
#
# @celery.task(name="create_task")
# def create_task(task_type):
#     '''Create a Celery task'''
#
#     time.sleep(int(task_type) * 10)
#     return True
