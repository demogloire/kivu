from flask import render_template, flash, url_for, redirect, request, session
from .. import db, bcrypt
from ..models import Types 
from app.types.forms import TypesnomForm, TypesedForm
from flask_login import login_user, current_user, logout_user, login_required
from . import types



''' Ajoute une classification '''

@types.route('/ajou_classe', methods=['GET', 'POST'])
@login_required
def typeclas():

   #La modification du mot de passe par l'administrateur.
   if current_user.role!='Admin':
      return redirect(url_for('main.dashboard'))
      
   #Titre
   title='Classification | Kivu Exchange'
   #formulaire
   form=TypesnomForm()

   if form.validate_on_submit():
      nom_clasification=form.nom.data.capitalize()
      classi=Types(nom=nom_clasification)
      db.session.add(classi)
      db.session.commit()
      flash("Ajout d'une nouvelle classification",'success')
      return redirect(url_for('types.litype')) 

   return render_template('types/ajtype.html',  title=title, form=form)

""" Liste des types """

@types.route('/lis_cat', methods=['GET', 'POST'])
@login_required
def litype():
   
   #La modification du mot de passe par l'administrateur.
   if current_user.role!='Admin':
      return redirect(url_for('main.dashboard'))

   #Titre
   title='Classification | Kivu Exchange'
   #Requête d'affichage des utlisateurs
   listes=Types.query.order_by(Types.id.desc())

   return render_template('types/views.html',title=title, liste=listes)


""" Modification du type  """

@types.route('/edit_<int:type_id>_type', methods=['GET', 'POST'])
@login_required
def edittype(type_id):
       
   #La modification du mot de passe par l'administrateur.
   if current_user.role!='Admin':
      return redirect(url_for('main.dashboard'))
   
   form=TypesedForm()
   #Titre
   title='Classification | Kivu Exchange'
   #Requête de vérification du type
   type_class=Types.query.filter_by(id=type_id).first()
   #Le nom du type encours de modification
   type_nom=type_class.nom

   if type_class is None:
      return redirect(url_for('types.litype'))
   
   if form.validate_on_submit(): 
      type_class.nom=form.ed_nom.data.capitalize()
      db.session.commit()
      flash("Modification réussie",'success')
      return redirect(url_for('types.litype')) 
   
   if request.method=='GET':
      form.ed_nom.data=type_class.nom

   return render_template('types/editype.html', form=form, title=title, type_nom=type_nom)

