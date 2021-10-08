from flask_wtf import FlaskForm
from wtforms import (MultipleFileField, SubmitField,
                     RadioField, IntegerField)
from wtforms_components import ColorField
from wtforms.validators import InputRequired, NumberRange
from wtforms.widgets import html5


class UploadForm(FlaskForm):
    images = MultipleFileField('images')
    submit = SubmitField('UPLOAD')


class ImageSettingsForm(FlaskForm):
    orientation = RadioField('Orientation', default='horizontal',
                             choices=[('horizontal', 'Horizontal Collage'),
                                      ('vertical', 'Vertical Collage')])
    background = ColorField('Background Color', validators=[InputRequired()])
    border = IntegerField(validators=[NumberRange(min=0, max=100)])
    border = IntegerField('Border', widget=html5.NumberInput(min=0, max=100,
                                                             step=1))
    submit = SubmitField('GENERATE COLLAGE')
