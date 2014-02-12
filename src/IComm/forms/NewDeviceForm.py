from flask_wtf import Form
from wtforms import TextField, SelectField
from wtforms.validators import DataRequired

class NewDeviceForm(Form):
    physic_id = TextField('Id physique', validators=[DataRequired()])
    name = TextField('Nom', validators=[DataRequired()])
    device_type = SelectField('Type', choices=[('temperature','Temperature'),('switch','Interrupteur')])