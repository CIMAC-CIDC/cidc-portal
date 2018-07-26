from wtforms import Form
from wtforms import StringField
from wtforms import BooleanField
from wtforms import validators


class RegistrationForm(Form):
    email = StringField("Username")
    contact_email = StringField("Preferred contact e-mail", [validators.InputRequired()])
    organization = StringField("Organization", [validators.InputRequired()])
    first_n = StringField("First Name", [validators.InputRequired()])
    last_n = StringField("Last Name", [validators.InputRequired()])
    cidc_role = StringField("What is your role in the CIMAC-CIDC Project?", [validators.InputRequired()])
    coc_signed = BooleanField("I have read and agree to the Code of Conduct", [validators.InputRequired()])
