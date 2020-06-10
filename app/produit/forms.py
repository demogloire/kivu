from flask_wtf import FlaskForm
from flask_wtf.file import FileField, FileAllowed
from flask_wtf.html5 import URLField
from wtforms import StringField, PasswordField, SubmitField, BooleanField, TextAreaField, SelectField, IntegerField, DecimalField
from wtforms.validators import DataRequired, Length,Email, EqualTo, ValidationError, url
from wtforms.ext.sqlalchemy.fields import QuerySelectField

from ..models import Types, Categorie

def rech_cate():
    return Categorie.query.filter_by(statut=True)

class AjoutProForm(FlaskForm):
    nom= StringField('Nom', validators=[DataRequired("Completer nom"),  Length(min=4, max=32, message="Veuillez respecté les caractères")])
    prix_p= DecimalField('Prix', validators=[DataRequired("Le prix du produit")])
    img_url=URLField('URL')
    mesure= StringField('Unité de mesure', validators=[DataRequired("Unité de mesure"),  Length(min=4, max=32, message="Veuillez respecté les caractères")])
    resume= TextAreaField('Contenu', validators=[DataRequired("Completer le contenu")])
    resume_android= TextAreaField('Contenu', validators=[DataRequired("Completer le contenu")])
    rech_cate= QuerySelectField(query_factory=rech_cate, get_label='nom', allow_blank=False)
    submit = SubmitField('Produit')

class AjoutPhoForm(FlaskForm):
    file = FileField("Image",validators=[FileAllowed(['jpg','png'],'Seul jpg et png sont autorisés')])
    submit = SubmitField('Produit')

class EdProForm(FlaskForm):
    ed_nom= StringField('Nom', validators=[DataRequired("Completer nom"),  Length(min=4, max=32, message="Veuillez respecté les caractères")])
    ed_prix_p= DecimalField('Prix', validators=[DataRequired("Le prix du produit")])
    ed_img_url=URLField('URL')
    resume_android= TextAreaField('Contenu', validators=[DataRequired("Completer le contenu")])
    ed_rech_cate= QuerySelectField(query_factory=rech_cate, get_label='nom', allow_blank=False)
    mesure= StringField('Unité de mesure', validators=[DataRequired("Unité de mesure"),  Length(min=4, max=32, message="Veuillez respecté les caractères")])
    resume= TextAreaField('Contenu', validators=[DataRequired("Completer le contenu")])
    submit = SubmitField('Produit')

class EdPhoForm(FlaskForm):
    ed_file = FileField("Image",validators=[FileAllowed(['jpg','png'],'Seul jpg et png sont autorisés')])
    submit = SubmitField('Produit')