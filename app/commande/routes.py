from datetime import datetime
from flask import render_template, flash, url_for, redirect, request, session
from .. import db, bcrypt
from ..models import Types, Categorie, Produit, Commandes
#from app.produit.forms import AjoutProForm, AjoutPhoForm, EdProForm,EdPhoForm
from flask_login import login_user, current_user, logout_user, login_required
from sqlalchemy.sql import func
from cloudinary.uploader import upload
from cloudinary.utils import cloudinary_url


from . import commande



''' Commande encours'''


@commande.route('/<int:commande_id> ', methods=['GET', 'POST'])
@login_required
def livraison_commande(commande_id):
   #Titre
   title='Commande | Kivu Exchanges'
   #verification de l'administrateur.
   if current_user.role!='Admin':
      return redirect(url_for('main.dashboard'))
   #Requête de vérification du commannde
   commande_liv_statu=Commandes.query.filter_by(id=commande_id).first_or_404()

   if commande_liv_statu.statut_liv == True:
      flash("Cette est déjà livrée",'danger')
   else:
      commande_liv_statu.statut_liv=True
      commande_liv_statu.date_commande=datetime.utcnow()
      db.session.commit()
      flash("La livraison de la commande confirmée",'success')
      return redirect(url_for('commande.commande'))
   
   return render_template('user/views.html',title=title)


@commande.route('/annuler/<int:commande_id> ', methods=['GET', 'POST'])
@login_required
def annule_commande(commande_id):
   #Titre
   title='Commande | Kivu Exchanges'
   #verification de l'administrateur.
   if current_user.role!='Admin':
      return redirect(url_for('main.dashboard'))
   #Requête de vérification du commannde
   commande_liv_statu=Commandes.query.filter_by(id=commande_id).first_or_404()

   if commande_liv_statu.annul_liv == True:
      flash("La commande annulée",'danger')
   else:
      commande_liv_statu.annul_liv=True
      db.session.commit()
      flash("Commande annulée", "success")
      return redirect(url_for('commande.commande'))
   
   



@commande.route('/<int:commande_id>/commande ', methods=['GET', 'POST'])
@login_required
def voir(commande_id):
   #Titre
   title='Commande | Kivu Exchanges'
   #verification de l'administrateur.
   if current_user.role!='Admin':
      return redirect(url_for('main.dashboard'))
   #Requête de vérification du commannde
   commande_liv_statu=Commandes.query.filter_by(id=commande_id).first_or_404()
   
   return render_template('commande/viewsdo.html',title=title, commande_liv_statu=commande_liv_statu)



@commande.route('/lescommandes', methods=['GET', 'POST'])
@login_required
def commande():
   #La modification du mot de passe par l'administrateur.
   if current_user.role!='Admin':
      return redirect(url_for('main.dashboard'))
   #Titre
   title='Commande | Kivu Exchange'
   #Requet des pagination et des listage des données
   page= request.args.get('page', 1, type=int)
   commande_page=Commandes.query.filter_by(annul_liv=False).order_by(Commandes.date_commande_liv.asc()).paginate(page=page, per_page=50)
   return render_template('commande/views.html', title=title, liste=commande_page)