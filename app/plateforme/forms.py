from flask_wtf import FlaskForm
from flask_wtf.file import FileField, FileAllowed
from wtforms import StringField, PasswordField, SubmitField, BooleanField, TextAreaField, SelectField, IntegerField, DecimalField
from wtforms.validators import DataRequired, Length,Email, EqualTo, ValidationError
from wtforms.ext.sqlalchemy.fields import QuerySelectField
import re
from ..models import User


class CommanderForm(FlaskForm):
    qte= IntegerField('Quantité', validators=[DataRequired("Completer la quantité")])
    nom= StringField('Nom', validators=[DataRequired("Completer nom"),  Length(min=2, max=32, message="Veuillez respecté les caractères")])
    tel= StringField('Téléphone', validators=[DataRequired("Completer le numero de téléphone"),  Length(min=6, max=32, message="Veuillez respecté les caractères")])
    email= StringField('Email', validators=[DataRequired('Veuillez completer votre email'), Email('Votre email est incorrect')])
    adresse= StringField('Nom', validators=[DataRequired("Completer nom")])
    submit = SubmitField('Envoyer')

    #Fornction de verification d'unique existenace dans la base des données
    def validate_qte(self, qte):
        qte=qte.data
        if  qte < 0 or qte == 0 :
            raise ValidationError("Quanntité doit être superieure à Zero")
    def validate_tel(self, tel):
        tel=tel.data
        ver='^(00|\+[1-9] )[1-9]'
        result = re.match(ver, tel)
        if result:
            pass
        else:
            raise ValidationError("La forme du numéro de téléphone est ex: 002439999999999")

class ColisPForm(FlaskForm):
    numero= StringField('Numero de colis', validators=[DataRequired('Le numéro de colis')])
    colis = SubmitField('le numero ')

class ColisForm(FlaskForm):
    numero= StringField('Numero de colis', validators=[DataRequired('Le numéro de colis')])
    submit = SubmitField('le numero ')


class DevisForm(FlaskForm):
    nom= StringField('Nom', validators=[DataRequired("Completer nom"),  Length(min=2, max=32, message="Veuillez respecté les caractères")])
    email= StringField('Email', validators=[DataRequired('Veuillez completer votre email'), Email('Votre email est incorrect')])
    devis = SubmitField('Envoyer')


