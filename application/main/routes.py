'''
application/main/routes.py

'''

import ast
import random
import string
import imghdr
from os import environ
from datetime import datetime as dt
from flask import (Blueprint, render_template, request, abort, redirect,
                   jsonify, url_for, flash, session, send_from_directory)
from flask_uploads import IMAGES, UploadSet
from flask_uploads.exceptions import UploadNotAllowed
from application.forms import UploadForm, ImageSettingsForm
from ..tasks import resize_image, merge_images

main = Blueprint('main', __name__,
                 template_folder='templates',
                 static_folder='static')

default_path = environ.get('UPLOADED_IMAGES_DEST')
images = UploadSet('images', IMAGES)


def is_image_valid(image):
    '''Check if image is valid'''

    valid_image = imghdr.what(image)
    return valid_image in ('png', 'jpeg')


def rename_image_file(filename):
    '''Rename files using a random string'''

    extention = filename[-3:]
    chars = ''.join(string.ascii_letters)
    filename = ''.join(random.choice(chars) for _ in range(16))
    return f'{filename}.{extention}'


def check_quantity(files):
    '''Set a limit on the number of files to upload'''

    if len(files) < 2:
        flash('At least 2 images are required.', 'failure')
        return True
    if len(files) > 6:
        flash('Maximum number of images exceeded.', 'failure')
        return True
    return None


def save_image_file(image_file):
    '''Try to save the uploaded image on server'''

    try:
        images.save(image_file)
    except UploadNotAllowed:
        flash('File type not allowed.', 'failure')
        return redirect(url_for('main.index', _external=True))
    return None


@main.get('/')
def index():
    '''Index route'''

    form = UploadForm()
    return render_template('main/index.html', form=form)


@main.post('/')
def uploads():
    '''Display uploaded images'''

    all_files = []
    file_obj = request.files.getlist('images')
    if check_quantity(file_obj):
        return redirect(url_for('main.index', _external=True))
    for img in file_obj:
        if is_image_valid(img) is False:
            flash('Not a valid image file.', 'failure')
            return redirect(url_for('main.index', _external=True))
        img.filename = rename_image_file(img.filename)
        save_image_file(img)
        all_files.append(img.filename)
        session['uploads'] = all_files
    flash('Photos uploaded successfully', 'success')
    return redirect(url_for('main.workspace', _external=True))


@main.route('/queue', methods=['GET', 'POST'])
def get_status():
    '''Get task ID route'''

    task = merge_images.AsyncResult(session['task_id'])
    print(f'TASK: {task}')
    print(f'STATE: {task.state}')
    print(f'READY: {task.ready()}')
    print(f'STATUS: {task.status}')
    if task.state == 'PENDING':
        result = {
                'state': task.ready(),
                'status': task.status
                }
    else:
        result = {
                'state': task.ready(),
                'status': task.status
                }
    return jsonify(result)


def set_default_background(background_color):
    '''Set default background to transparent'''

    if background_color == '#000001':
        return (0, 0, 0, 0)
    return (0, 0, 1, 1)


@main.get('/workspace')
def workspace():
    '''Workspace route'''

    form = ImageSettingsForm()
    return render_template('main/workspace.html',
                           form=form, files=session['uploads'])


@main.route('/generate/<images>', methods=['GET', 'POST'])
async def create_collage(images):
    '''Create collage of the images'''

    form = ImageSettingsForm()
    images_list = ast.literal_eval(images)

    if form.validate_on_submit():
        border = int(request.form.get('border'))
        background = set_default_background(request.form.get('background'))
        orientation = request.form.get('orientation')
        all_images = resize_image(images_list, 500, border, background)
        filename = f'collage_{dt.utcnow().strftime("%Y%m%d-%H%M%S.%f")}.png'
        task = merge_images.apply_async(args=[all_images, filename,
                                        orientation], countdown=2)
        session['task_id'] = task.id
        session['collage'] = filename
        return redirect(url_for('main.display_collage', _external=True))
    return render_template('main/workspace.html', form=form)


@main.route('/download/<filename>')
def download_image(filename):
    '''Download collage image'''

    path = environ.get('DOWNLOAD_URL')
    try:
        return send_from_directory(path, session['collage'],
                                   as_attachment=True)
    except FileNotFoundError:
        abort(404)
    return None


@main.get('/result')
def display_collage():
    '''Display collage to download'''

    return render_template('main/result.html', image=session['collage'])


@main.get('/privacy_policy')
def privacy_policy():
    '''Privacy Policy'''

    return render_template('main/privacy_policy.html')


@main.get('/terms_of_service')
def terms_of_service():
    '''Terms Of Service'''

    return render_template('main/terms_of_service.html')


@main.app_errorhandler(404)
def page_not_found(error):
    '''404 Page not found'''

    return render_template('404.html'), 404


@main.app_errorhandler(413)
def file_too_large(error):
    '''413 Request Entity Too Large'''

    return render_template('413.html'), 413


@main.app_errorhandler(500)
def internal_server_error(error):
    '''500 Internal server error'''

    return render_template('500.html'), 500
