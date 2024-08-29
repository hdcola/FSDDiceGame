from flask_wtf import FlaskForm
from wtforms import StringField
from wtforms.validators import DataRequired


class StartForm(FlaskForm):
    player1 = StringField('Name 1', validators=[DataRequired()])
    player2 = StringField('Name 2', validators=[DataRequired()])
