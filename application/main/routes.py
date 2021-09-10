import ast
import random
import string
from os import environ
from pathlib import Path
from datetime import datetime
from PIL import Image, ImageOps
import numpy
from flask import (Blueprint, render_template, request, abort, redirect,
                   jsonify, json, url_for, flash, session, send_from_directory)
from flask_uploads import IMAGES, UploadSet
from celery.result import AsyncResult
from ..tasks import (
                     # resize_image,
                     save_images_to,
                     create_thumbnail)
from application.forms import UploadForm

main = Blueprint('main', __name__,
                 template_folder='templates',
                 static_folder='static')

default_path = environ.get('UPLOADED_IMAGES_DEST')
images = UploadSet('images', IMAGES)


@main.get('/')
def index():
    '''Index route'''

    form = UploadForm()
    return render_template('main/index.html', form=form)


@main.post('/')
def uploads():
    '''Display uploaded images'''

    all_files = []
    all_tasks = []
    chars = ''.join(string.ascii_letters)
    form = UploadForm()
    if request.method == 'POST':
        file_obj = request.files.getlist('images')
        if len(file_obj) < 2:
            flash('At least 2 images are required.', 'failure')
            return redirect(url_for('main.index'))
        if len(file_obj) > 5:
            flash('Maximum number of images exceeded.', 'failure')
            return redirect(url_for('main.index'))
        for img in file_obj:
            filename = ''.join(random.choice(chars) for _ in range(16))
            img.filename = f'{filename}.{img.filename.split(".")[1]}'
            images.save(img)
            all_files.append(img.filename)
            # task = create_thumbnail.delay(img.filename)
            task = create_thumbnail.apply_async(args=[img.filename],
                                                countdown=10)
            all_tasks.append(task.task_id)
            print(task.task_id)
            print(task.status)
            print(task.state)
            session['uploads'] = all_files
        session['tasks_ids'] = all_tasks
        # print(session['tasks'])
        flash('Photos uploaded successfully', 'success')
        return redirect(url_for('main.workspace'))
    return render_template('main/index.html', form=form, files=all_files)


@main.route('/queue/<task_id>')
def get_status(task_id):

    # results = []
    # for i in session['tasks_ids']:
    #     task = create_thumbnail.AsyncResult(i).status
    #     results.append(task)
    # results = json.dumps(results)
    # results = datetime.utcnow().strftime("%S")
    results = create_thumbnail.AsyncResult(task_id).status
    return results


@main.get('/status/<task_id>')
def task_status(task_id):

    task = create_thumbnail.AsyncResult(task_id)
    return jsonify(task)


@main.get('/workspace')
def workspace(uploads=None):

    form = UploadForm()
    return render_template('main/workspace.html',
                           form=form, files=session['uploads'])


@main.route('/generate/<images>', methods=['GET', 'POST'])
def create_collage(images, size=500):
    '''Create collage of the images'''

    form = UploadForm()
    all_images = []
    images = ast.literal_eval(images)
    location = save_images_to(default_path)

    if form.validate_on_submit():
        border = request.form.get('border')
        background = request.form.get('background')
        orientation = request.form.get('orientation')
        # for img in images:
        # resized_pic = resize_image.apply_async(args=[img, border,
        #                                          background, 500], countdown=30)
        # ---------------------------------------------------
        open_files = [Image.open(Path(location / img)) for img in images]
        convert_to_png = [img.convert('RGBA') for img in open_files]
        resized_pic = [img.resize((500, 500)) for img in convert_to_png]
        expand_border = [ImageOps.expand(img, border=int(border),
                         fill=background) for img in resized_pic]
        img_array = [numpy.asarray(img) for img in expand_border]
        all_images = [img for img in img_array]
        # ---------------------------------------------------
        # print(resized_pic.task_id)
        # pic_arr = numpy.array(resized_pic)
        # all_images.append(resized_pic)
        # if orientation == 'vertical':
        # merged_images = merge_images.delay(all_images, 'vertical')
        # pass
        # else:
        #     merged_images = merge_images.delay(all_images)
        # pass
        # ---------------------------------------------------
        image_array = [numpy.asarray(img) for img in all_images]
        images_list = []
        for img in image_array:
            images_list.append(img)
        if orientation == 'vertical':
            merged_images = numpy.vstack((images_list))
        else:
            merged_images = numpy.hstack((images_list))
        collage = Image.fromarray(merged_images)
        filename = f'collage_{datetime.utcnow().strftime("%Y%m%d%H%M%S")}.png'
        collage.save(Path(location / filename))
        # ---------------------------------------------------
        # collage = Image.fromarray(merged_images, 'RGB')
        # collage = merge_images(all_images)
        # collage.save(Path(location / 'photo-collage.png'))
        # collage.save(Path(location / 'photo-collage.png'))
        # filename = Path(location / 'photo-collage.png')
        session['collage'] = filename
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
