from wtforms import Form
from wtforms import StringField
from wtforms import SelectField
from wtforms import BooleanField
from wtforms import validators

ORGANIZATIONS = [("DFCI", "Dana-Farber Cancer Institute"),
                 ("MDACC", "MD Anderson Cancer Center"),
                 ("MS", "Mount Sinai"),
                 ("SU", "Stanford University")]

CIDC_ROLE = [("CIMAC_UPLOADER", "CIMAC Data Uploader"),
             ("CIMAC_BIOINFO", "CIMAC Bioinformatician"),
             ("CIDC_BIOINFO", "CIDC Bioinformatician"),
             ("CIDC_DEVELOPER", "CIDC Developer")]


class RegistrationForm(Form):
    email = StringField("Username")
    contact_email = StringField("Preferred contact e-mail", [validators.InputRequired(), validators.Email()])

    organization = SelectField("Organization",
                               choices=ORGANIZATIONS
                               )

    first_n = StringField("First Name", [validators.InputRequired(),
                                         validators.Regexp('^[a-zA-Z\s]*$',
                                                           message="Your First Name name can "
                                                                   "only contain letters and spaces.")
                                         ])
    last_n = StringField("Last Name", [validators.InputRequired(),
                                       validators.Regexp('^[a-zA-Z\s]*$',
                                                         message="Your Last Name name can "
                                                                 "only contain letters and spaces.")
                                       ])

    cidc_role = SelectField("What is your role in the CIMAC-CIDC Project?", choices=CIDC_ROLE)
    coc_signed = BooleanField("I have read and agree to the Code of Conduct", [validators.InputRequired()])
