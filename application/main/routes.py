import ast
from os import environ
from pathlib import Path
from PIL import Image
import numpy
from flask import (Blueprint, render_template, request, abort,
                   redirect, url_for, flash, session, send_from_directory)
from flask_uploads import IMAGES, UploadSet
from ..tasks import (resize_image, save_images_to,
                     create_thumbnail)
from application.forms import UploadForm

main = Blueprint('main', __name__,
                 template_folder='templates',
                 static_folder='static')

default_path = environ.get('UPLOADED_IMAGES_DEST')
images = UploadSet('images', IMAGES)


@main.route('/', methods=['GET'])
def index():
    '''Index route'''

    form = UploadForm()
    return render_template('main/index.html', form=form)


@main.route('/', methods=['POST'])
def uploads():
    '''Display uploaded images'''

    all_files = []
    form = UploadForm()
    if request.method == 'POST':
        file_obj = request.files.getlist('images')
        if len(file_obj) < 2:
            flash('At least 2 images are required.', 'failure')
            return redirect(url_for('main.index'))
        for img in file_obj:
            images.save(img)
            all_files.append(img.filename)
            create_thumbnail(img.filename)
            session['uploads'] = all_files
        flash('Photos uploaded successfully', 'success')
        return redirect(url_for('main.workspace'))
    return render_template('main/index.html', form=form, files=all_files)


@main.route('/workspace')
def workspace(uploads=None):

    form = UploadForm()
    return render_template('main/workspace.html',
                           form=form, files=session['uploads'])


@main.route('/generate/<images>', methods=['GET', 'POST'])
def create_collage(images, size=500, direction='horizontal'):
    '''Create collage of the images'''

    form = UploadForm()
    all_images = []
    images = ast.literal_eval(images)
    location = save_images_to(default_path)
    if form.validate_on_submit():
        # for img in images:
            #resized_pic = resize_image.delay(img, size)
            # ---------------------------------------------------
        open_files = [Image.open(Path(location / x)) for x in images]
        convert_to_png = [x.convert('RGBA') for x in open_files]
        resized_pic = [x.resize((400, 400)) for x in convert_to_png]
        img_array = [numpy.asarray(x) for x in resized_pic]
        all_images = [i for i in img_array]
            # print(resized_pic.task_id)
            # pic_arr = numpy.array(resized_pic)
            # all_images.append(resized_pic)
        if direction == 'vertical':
            # merged_images = merge_images.delay(all_images, 'vertical')
            pass
        else:
        #     merged_images = merge_images.delay(all_images)
            pass
        # ---------------------------------------------------
        image_array = [numpy.asarray(img) for img in all_images]
        images_list = []
        for img in image_array:
            images_list.append(img)
        merged_images = numpy.hstack((images_list))
        collage = Image.fromarray(merged_images)
        collage.save(Path(location / 'photo-collage-new.png'))
        # ---------------------------------------------------
        # collage = Image.fromarray(merged_images, 'RGB')
        # collage = merge_images(all_images)
        # collage.save(Path(location / 'photo-collage.png'))
        # collage.save(Path(location / 'photo-collage.png'))
        # filename = Path(location / 'photo-collage.png')
        session['collage'] = 'photo-collage-new.png'
        # session['collage'] = filename
        # return redirect(url_for('main.collage'))
        return redirect(url_for('main.display_collage'))
    return render_template('main/workspace.html', form=form)


@main.route('/download')
def download_image():
    '''Download image'''

    try:
        return send_from_directory(environ.get('UPLOADED_IMAGES_DEST'),
                                   default_path,
                                   filename=session['collage'],
                                   as_attachment=True)
    except FileNotFoundError:
        abort(404)


@main.route('/result')
def display_collage():
    '''Display collage to download'''

    return render_template('main/result.html', image=session['collage'])


@main.route('/privacy_policy')
def privacy_policy():
    '''Privacy Policy'''

    return render_template('main/privacy_policy.html')


@main.route('/terms_of_service')
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
