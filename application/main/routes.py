# application/main/routes.py

import ast
import random
import string
import imghdr
from os import environ
from flask import (Blueprint, render_template, request, abort, redirect,
                   jsonify, url_for, flash, session, send_from_directory)
from flask_uploads import IMAGES, UploadSet
from flask_uploads.exceptions import UploadNotAllowed
# from celery.result import AsyncResult
from ..tasks import merge_images, generate_collage
from application.forms import UploadForm, ImageSettingsForm

main = Blueprint('main', __name__,
                 template_folder='templates',
                 static_folder='static')

default_path = environ.get('UPLOADED_IMAGES_DEST')
images = UploadSet('images', IMAGES)


def is_image_valid(image):
    '''Check if image is valid'''

    valid_image = imghdr.what(image)
    return valid_image == 'png' or valid_image == 'jpeg'


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


def save_image_file(image_file):
    '''Try to save the image file'''

    try:
        images.save(image_file)
    except UploadNotAllowed:
        flash('File type not allowed.', 'failure')
        return redirect(url_for('main.index'))


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
        return redirect(url_for('main.index'))
    for img in file_obj:
        if is_image_valid(img) is False:
            flash('Not a valid image file.', 'failure')
            return redirect(url_for('main.index'))
        img.filename = rename_image_file(img.filename)
        save_image_file(img)
        all_files.append(img.filename)
        session['uploads'] = all_files
    flash('Photos uploaded successfully', 'success')
    return redirect(url_for('main.workspace'))


@main.route('/queue/<task_id>')
def get_status(task_id):
    '''Get task ID route'''

    task = generate_collage.AsyncResult(task_id)
    return task


@main.get('/status/<task_id>')
def task_status(task_id):
    '''Task ID route'''

    task = merge_images.AsyncResult(task_id)
    response = task.state
    return jsonify(response)


def set_default_background(bg_color):
    '''Set default background to transparent'''

    if bg_color == '#000001':
        return (0, 0, 0, 0)


@main.get('/workspace')
def workspace(uploads=None):
    '''Workspace route'''

    form = ImageSettingsForm()
    return render_template('main/workspace.html',
                           form=form, files=session['uploads'])


@main.route('/generate/<images>', methods=['GET', 'POST'])
def create_collage(images, size=500):
    '''Create collage of the images'''

    form = ImageSettingsForm()
    images = ast.literal_eval(images)

    if form.validate_on_submit():
        border = request.form.get('border')
        background = set_default_background(request.form.get('background'))
        orientation = request.form.get('orientation')
        merged_images = [merge_images(img, border, background)
                         for img in images]
        # collage = generate_collage(merged_images, orientation)
        # collage = generate_collage.apply_async(args=[merged_images,
        #                                        orientation],
        #                                        serializer='json')
        collage = generate_collage(merged_images, orientation)
        session['collage'] = collage
        return redirect(url_for('main.display_collage'))
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


@main.app_errorhandler(500)
def internal_server_error(error):
    '''500 Internal server error'''

    return render_template('500.html'), 500
