from flask_wtf import FlaskForm
from wtforms import FileField


class UploadForm(FlaskForm):
    image = FileField('image')
