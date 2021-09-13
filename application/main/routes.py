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
from application.forms import UploadForm

main = Blueprint('main', __name__,
                 template_folder='templates',
                 static_folder='static')

default_path = environ.get('UPLOADED_IMAGES_DEST')
images = UploadSet('images', IMAGES)


def is_image_valid(image):
    '''Check if image is valid'''

    if imghdr.what(image) == 'png' or imghdr.what(image) == 'jpeg':
        return True
    else:
        return False


@main.get('/')
def index():
    '''Index route'''

    form = UploadForm()
    return render_template('main/index.html', form=form)


@main.post('/')
def uploads():
    '''Display uploaded images'''

    all_files = []
    chars = ''.join(string.ascii_letters)
    form = UploadForm()
    if request.method == 'POST':
        file_obj = request.files.getlist('images')
        if len(file_obj) < 2:
            flash('At least 2 images are required.', 'failure')
            return redirect(url_for('main.index'))
        if len(file_obj) > 6:
            flash('Maximum number of images exceeded.', 'failure')
            return redirect(url_for('main.index'))
        for img in file_obj:
            if is_image_valid(img) is False:
                flash('Not a valid image file.', 'failure')
                return redirect(url_for('main.index'))
            filename = ''.join(random.choice(chars) for _ in range(16))
            img.filename = f'{filename}.{img.filename[-3:]}'
            try:
                images.save(img)
            except UploadNotAllowed:
                flash('File type not allowed.', 'failure')
                return redirect(url_for('main.index'))
            all_files.append(img.filename)
            session['uploads'] = all_files
        flash('Photos uploaded successfully', 'success')
        return redirect(url_for('main.workspace'))
    return render_template('main/index.html', form=form, files=all_files)


@main.route('/queue/<task_id>')
def get_status(task_id):

    results = ''
    return results


@main.get('/status/<task_id>')
def task_status(task_id):

    task = merge_images.AsyncResult(task_id)
    response = task.state
    return jsonify(response)


@main.get('/workspace')
def workspace(uploads=None):

    form = UploadForm()
    return render_template('main/workspace.html',
                           form=form, files=session['uploads'])


@main.route('/generate/<images>', methods=['GET', 'POST'])
def create_collage(images, size=500):
    '''Create collage of the images'''

    form = UploadForm()
    images = ast.literal_eval(images)

    if form.validate_on_submit():
        border = request.form.get('border')
        background = request.form.get('background')
        if background == '#000000':
            background = (0, 0, 0, 0)
        orientation = request.form.get('orientation')
        merged_images = [merge_images(img, border, background)
                         for img in images]
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
