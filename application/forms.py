from flask_wtf import FlaskForm
from wtforms import FileField, SubmitField


class UploadForm(FlaskForm):
    images = FileField('images')
    submit = SubmitField('UPLOAD')
