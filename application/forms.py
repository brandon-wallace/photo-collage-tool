from flask_wtf import FlaskForm
from wtforms import FileField, SubmitField


class UploadForm(FlaskForm):
    image = FileField('image')
    submit = SubmitField('UPLOAD')
