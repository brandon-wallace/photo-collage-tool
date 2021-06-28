import secrets
from os import path
from PIL import Image
from flask import Blueprint, render_template, current_app
from flask_uploads import IMAGES, UploadSet
from application.forms import UploadForm

main = Blueprint('main', __name__,
                 template_folder='templates',
                 static_folder='static')

images = UploadSet('images', IMAGES)


@main.route('/', methods=['GET', 'POST'])
def index():
    '''Index route'''

    form = UploadForm()
    if form.validate_on_submit():
        filename = images.save(form.image.data)
        return filename

    return render_template('main/index.html', form=form)


def upload(image_file):
    '''Upload and save picture'''

    random_hex = secrets.token_hex(8)
    _, file_ext = path.splitext(image_file.filename)
    picture_filename = random_hex + file_ext
    picture_path = path.join(current_app.root_path,
                             'static/images', picture_filename)
    output_size = (125, 125)
    pic = Image.open(image_file)
    pic.thumbnail(output_size)
    pic.save(picture_path)

    return picture_filename


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
