from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField, FileField
from wtforms.validators import DataRequired


class FindForm(FlaskForm):
    information = StringField('Information', validators=[DataRequired()],
                              render_kw={"class": "form-control"})
    submit = SubmitField('Find')
