from flask_wtf import FlaskForm
from flask_wtf.file import FileField, FileAllowed
from wtforms import StringField, PasswordField, SubmitField, BooleanField, TextAreaField, SelectField, IntegerField, DecimalField
from wtforms.validators import DataRequired, Length,Email, EqualTo, ValidationError
from wtforms.ext.sqlalchemy.fields import QuerySelectField

from ..models import Types


class TypesnomForm(FlaskForm):
    nom= StringField('Nom', validators=[DataRequired("Completer nom"),  Length(min=4, max=32, message="Veuillez respecté les caractères")])
    submit = SubmitField('Classification')

    #Fornction de verification d'unique existenace dans la base des données
    def validate_nom(self, nom):
        type= Types.query.filter_by(nom=nom.data).first()
        if type:
            raise ValidationError("Cette classification existe déjà")

class TypesedForm(FlaskForm):
    ed_nom= StringField('Nom', validators=[DataRequired("Completer nom"),  Length(min=4, max=32, message="Veuillez respecté les caractères")])
    ed_submit = SubmitField('Classification')

    #Fornction de verification d'unique existenace dans la base des données
    def validate_ed_nom(self, ed_nom):
        type= Types.query.filter_by(nom=ed_nom.data).first()
        if type:
            raise ValidationError("Cette classification existe déjà")
