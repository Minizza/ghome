from flask_wtf import Form
from wtforms import TextField, SelectField
from wtforms.validators import DataRequired

from Model.Device.DeviceFactory import DeviceFactory

class NewDeviceForm(Form):
    physic_id = TextField('Id physique', validators=[DataRequired()])
    name = TextField('Nom', validators=[DataRequired()])
    device_type = SelectField('Type', choices=DeviceFactory.getTypes())