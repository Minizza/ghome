from flask_wtf import Form
from wtforms import TextField
from wtforms.validators import DataRequired

class NewDeviceForm(Form):
    physic_id = TextField('Id physique', validators=[DataRequired()])
    name = TextField('Nom', validators=[DataRequired()])