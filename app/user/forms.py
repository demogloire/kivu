from flask_wtf import FlaskForm
from flask_wtf.file import FileField, FileAllowed
from wtforms import StringField, PasswordField, SubmitField, BooleanField, TextAreaField, SelectField, IntegerField, DecimalField
from wtforms.validators import DataRequired, Length,Email, EqualTo, ValidationError
from wtforms.ext.sqlalchemy.fields import QuerySelectField

from ..models import User

def rech_user():
    return Service.query.filter_by(active=True)

class AjouteruserForm(FlaskForm):
    nom= StringField('Nom', validators=[DataRequired("Completer nom"),  Length(min=4, max=32, message="Veuillez respecté les caractères")])
    post_nom= StringField('Post-nom', validators=[DataRequired("Completer nom"),  Length(min=4, max=32, message="Veuillez respecté les caractères")])
    prenom= StringField('Prénom', validators=[DataRequired("Completer nom"),  Length(min=4, max=32, message="Veuillez respecté les caractères")])
    username= StringField('Email', validators=[DataRequired('Veuillez completer votre email'), Email('Votre email est incorrect')])
    password= PasswordField('Mot de passe', validators=[DataRequired('Veuillez completer votre mot de passe')])
    role= SelectField('Rôle',choices=[('Admin', 'Admin'), ('Webmaster', 'Webmaster')])
    submit = SubmitField('Créer compte')

    #Fornction de verification d'unique existenace dans la base des données
    def validate_username(self, username):
        user= User.query.filter_by(username=username.data).first()
        if user:
            raise ValidationError("Cet utilisateur existe déjà")

class EditeruserForm(FlaskForm):
    ed_nom= StringField('Nom', validators=[DataRequired("Completer nom"),  Length(min=4, max=32, message="Veuillez respecté les caractères")])
    ed_post_nom= StringField('Post-nom', validators=[DataRequired("Completer nom"),  Length(min=4, max=32, message="Veuillez respecté les caractères")])
    ed_prenom= StringField('Prénom', validators=[DataRequired("Completer nom"),  Length(min=4, max=32, message="Veuillez respecté les caractères")])
    ed_username= StringField('Email', validators=[DataRequired('Veuillez completer votre email'), Email('Votre email est incorrect')])
    ed_role= SelectField('Rôle',choices=[('Admin', 'Admin'), ('Webmaster', 'Webmaster')])
    ed_submit = SubmitField('Créer compte')


class PassuserForm(FlaskForm):
    password= PasswordField('Mot de passe', validators=[DataRequired('Veuillez completer votre mot de passe')])
    confirm_password= PasswordField('Confirmer mot de passe', validators=[DataRequired('Veuillez completer votre mot de passe'), EqualTo('password',message="Les mots des passes ne pas conforment")])
    submit = SubmitField('Changer mot de passe')
    