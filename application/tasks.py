import time
from PIL import Image
from application import celery


@celery.task
def resize_image(img, size):
    '''Resize images'''

    pic = Image.open(img)
    resized_picture = pic.resize((size, size))
    return resized_picture


@celery.task
def make_list():
    '''Concatenation'''

    my_list = []
    for item in range(100000):
        my_list = my_list + [item]


@celery.task(name="create_task")
def create_task(task_type):
    '''Create a Celery task'''

    time.sleep(int(task_type) * 10)
    return True
