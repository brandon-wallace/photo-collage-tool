import ast
# from pathlib import Path
# from PIL import Image
# import numpy
from flask import (Blueprint, render_template, request,
                   redirect, url_for, flash, session)
from flask_uploads import IMAGES, UploadSet
from ..tasks import resize_image
from application.forms import UploadForm

main = Blueprint('main', __name__,
                 template_folder='templates',
                 static_folder='static')

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
        for img in file_obj:
            images.save(img)
            all_files.append(img.filename)
            session['uploads'] = all_files
        flash('Photos uploaded successfully', 'success')
        return redirect(url_for('main.workspace'))
    return render_template('main/index.html', form=form, files=all_files)


@main.route('/workspace')
def workspace(uploads=None):

    return render_template('main/workspace.html', files=session['uploads'])


@main.route('/generate/<images>', methods=['GET', 'POST'])
def create_collage(images, size=500, direction='horizontal'):
    '''Create collage of the images'''

    form = UploadForm()
    all_images = []
    images = ast.literal_eval(images)
    # src_directory = Path('uploads/images')
    for img in images:
        # pic = Image.open(Path(src_directory / img))
        # resized_pic = resize_image.delay(img, size)
        resized_pic = resize_image(img, size)
        print(resized_pic)
        # pic_arr = numpy.array(resized_pic)
        all_images.append(resized_pic)
    # print(all_images)
    # if direction == 'vertical':
    #     merged_images = numpy.vstack(all_images)
    # else:
    #     merged_images = numpy.hstack(all_images)
    # collage = Image.fromarray(merged_images)
    # collage.save(Path(src_directory / 'photo-collage.png'))
    return render_template('main/workspace.html', form=form)


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
