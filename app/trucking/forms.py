from flask_wtf import FlaskForm
from flask_wtf.file import FileField, FileAllowed
from wtforms import StringField, PasswordField, SubmitField, BooleanField, TextAreaField, SelectField, IntegerField, DecimalField, DateTimeField
from wtforms.validators import DataRequired, Length,Email, EqualTo, ValidationError
from wtforms.ext.sqlalchemy.fields import QuerySelectField
#from wtforms_components import CountryField

from ..models import Transit, Trucking


class AjouTrucking(FlaskForm):
    provenance= StringField('Provenance', validators=[DataRequired("Completer la ville")])
    destination=StringField('Provenance', validators=[DataRequired("Completer la ville")])
    date_envoi=DateTimeField('Date', format='%Y-%m-%d %H:%M:%S', validators=[DataRequired("Completer la date")])
    ville= StringField('Ville', validators=[DataRequired("Completer la ville")])
    submit = SubmitField('Trucking number')

class Datelivraison(FlaskForm):
    date_livraison=DateTimeField('Date', format='%Y-%m-%d %H:%M:%S', validators=[DataRequired("Completer la date")])
    submit = SubmitField('Trucking number')

class TransitTrucking(FlaskForm):
    en_transit=StringField('Provenance', validators=[DataRequired("Completer la ville")])
    ville= StringField('Ville', validators=[DataRequired("Completer la ville")])
    resume= TextAreaField(validators=[DataRequired("Commentaire ")])
    date_envoi=DateTimeField('Date', format='%Y-%m-%d %H:%M:%S', validators=[DataRequired("Completer la date")])
    submit = SubmitField('Trucking number')

class TransitModTrucking(FlaskForm):
    truckingnumber= StringField('Provenance', validators=[DataRequired("Completer la ville")])
    en_transit=StringField('Provenance', validators=[DataRequired("Completer la ville")])
    ville= StringField('Ville', validators=[DataRequired("Completer la ville")])
    resume= TextAreaField(validators=[DataRequired("Commentaire ")])
    submit = SubmitField('Trucking number')


class MofTrucking(FlaskForm):
    truckingnumber= StringField('Provenance', validators=[DataRequired("Completer la ville")])
    provenance= StringField('Provenance', validators=[DataRequired("Completer la ville")])
    destination=StringField('Destination', validators=[DataRequired("Completer la ville")])
    ville= StringField('Ville', validators=[DataRequired("Completer la ville")])
    submit = SubmitField('Trucking number')
