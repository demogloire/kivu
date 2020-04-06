from flask import render_template, flash, url_for, redirect, request, session
from .. import db, bcrypt
from ..models import User, Trucking, Transit, Produit, Commandes, Types, Categorie, Devis 
from app.plateforme.forms import CommanderForm, ColisForm, DevisForm, ColisPForm
from flask_login import login_user, current_user, logout_user, login_required
from . import plate


@plate.route('/', methods=['GET','POST'])
def index():
   title='Accueil | Kivu Exchange'
   produit=Produit.query.filter_by(statut=True).limit(3)
   slider=Produit.query.filter_by(statut=True).limit(20)
   return render_template('plateforme/acceuil.html',  title=title, produit=produit, slider=slider)

@plate.route('/apropos-de-nous.html', methods=['GET','POST'])
def aproposdenous():

   title='A propos de nous | Kivu Exchange'
   page_actuelle="A propos de nous"
   return render_template('plateforme/apropos.html', page=page_actuelle )



@plate.route('/ethiopian_fret', methods=['GET','POST'])
def suivis():
   title='Suivis colis | Kivu Exchange'
   form=ColisForm()
   trucking_id_client=None
   track_statu=None
   track_transit=None
   page_actuelle="Suivis de colis"
   suivi_notification=None
   if form.validate_on_submit():
      numero=Trucking.query.filter_by(tracking_number=form.numero.data).first()
      if numero is None:
         trucking_id_client=True
         flash("Aucun colis avec ce numéro","danger")
      else:
         trucking_id_client='requete'
         #Requête de vérification du trancking
         track_statu=Trucking.query.filter_by(tracking_number=form.numero.data, ).first()
         #Transit du colis.
         track_transit=Transit.query.filter_by(trucking_id=track_statu.id).all() 
      suivi_notification="Envoyer"

   colis=ColisPForm()
   if colis.validate_on_submit():
      numero=Trucking.query.filter_by(tracking_number=colis.numero.data).first()
      if numero is None:
         trucking_id_client=True
         flash("Aucun colis avec ce numéro","danger")
      else:
         trucking_id_client='requete'
         #Requête de vérification du trancking
         track_statu=Trucking.query.filter_by(tracking_number=colis.numero.data).first()
         #Transit du colis.
         track_transit=Transit.query.filter_by(trucking_id=track_statu.id).all()

      suivi_notification="Envoyer"

   
   devis=DevisForm()
   devis_notification=None
   if devis.validate_on_submit():
      enre_devis=Devis(nom=devis.nom.data.title(), email=devis.email.data)
      db.session.add(enre_devis)
      db.session.commit()
      flash("Le devis vous sera envoyé dans votre mail","success")
      devis_notification="Envoyer"
      
   return render_template('plateforme/suiviscolis.html', colis=colis, suivi_notification=suivi_notification, devis_notification=devis_notification, devis=devis, page=page_actuelle, trucking_id_client=trucking_id_client, truck=track_statu, track_transit=track_transit, title=title, form=form)

@plate.route('/nos-produits.html', methods=['GET','POST'])
def produit():
   title='Nos produits | Kivu Exchange'
   page_actuelle="Nos produits"
   page= request.args.get('page', 1, type=int)
   produit_page=Produit.query.filter_by(statut=True).order_by(Produit.id.desc()).paginate(page=page, per_page=50)
   ctr_pro="Vide"
   if produit_page is not None:
      ctr_pro="Novide"
   #Type de l'applicabilité
   typever="Vide"
   type_application=Types.query.filter_by(nom="E-commerce").first()
   if type_application is not None:
      typever="Novide"
   #Catégorie verification   
   categoriever="Vide"
   categorie_app=Categorie.query.filter_by(type_id=type_application.id, statut=True)
   if categorie_app is not None:
      categoriever="Novide"
      
   return render_template('plateforme/produits.html',categoriever=categoriever,typever=typever, categorie_app=categorie_app, page=page_actuelle, title=title, ctr_pro=ctr_pro, liste=produit_page)


@plate.route('/<int:cat_int>/nos-produits.html', methods=['GET','POST'])
def produit_categorie(cat_int):
   title='Catégorie | Kivu Exchange'
   
   page= request.args.get('page', 1, type=int)
   produit_page=Produit.query.filter_by(statut=True, categorie_id=cat_int).order_by(Produit.id.desc()).paginate(page=page, per_page=50)
   ctr_pro="Vide"
   if produit_page is not None:
      ctr_pro="Novide"
   #Type de l'applicabilité
   typever="Vide"
   type_application=Types.query.filter_by(nom="E-commerce").first()
   if type_application is not None:
      typever="Novide"
   #Catégorie verification   
   categoriever="Vide"
   categorie_app=Categorie.query.filter_by(type_id=type_application.id, statut=True)
   if categorie_app is not None:
      categoriever="Novide"
   categorie_sid=Categorie.query.filter_by(id=cat_int).first_or_404()
   page_actuelle="{}".format(categorie_sid.nom)

   return render_template('plateforme/catproduits.html',categorie_sid=categorie_sid, categoriever=categoriever,typever=typever, categorie_app=categorie_app, page=page_actuelle, title=title, ctr_pro=ctr_pro, liste=produit_page)



@plate.route('/<string:code>/produit.html', methods=['GET','POST'])
def commandepro(code):

   produit=Produit.query.filter_by(code=code,statut=True).first_or_404()
   #Verification de l'existence du produit
   title=" {} | Kivu Exchange".format(produit.nom)
   page_actuelle=" {} ".format(produit.nom)
   form=CommanderForm()
   categorie=Produit.query.filter_by(categorie_id=produit.categorie_id,statut=True)

   if form.validate_on_submit():
      qte=form.qte.data #Quantité commandée
      somme=qte * produit.prix_p
      commandeproduit=Commandes(qte=qte, somme=somme, nom_client=form.nom.data.upper(), tel=form.tel.data, mail=form.email.data,\
                                 adr=form.adresse.data, produit_id=produit.id)
      db.session.add(commandeproduit)
      db.session.commit()
      flash("Commande reussie, on vous contactera pour confirmer votre commande",'success')
      return redirect(url_for('plate.commandepro', code=code))

   
   
   return render_template('plateforme/commande.html', page=page_actuelle, title=title, produit=produit, form=form, categorie=categorie)


@plate.route('/contactez-nous.html', methods=['GET','POST'])
def contact():

   title='Contactez-nous | Kivu Exchange'
   page_actuelle="Contactez-nous"
   return render_template('plateforme/contact.html', page=page_actuelle )