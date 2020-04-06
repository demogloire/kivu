from flask import render_template, flash, url_for, redirect, request, session
from .. import db, bcrypt
from datetime import date, datetime 
from ..models import Trucking, Transit, Devis
from app.trucking.forms import AjouTrucking, TransitTrucking, Datelivraison, MofTrucking, TransitModTrucking
from app.trucking.utiliescode import trucking_number, truckin_id
from flask_login import login_user, current_user, logout_user, login_required
import time

from . import trucking



''' Ajoute un numero de trucking number '''

@trucking.route('/ajoutrucking', methods=['GET', 'POST'])
@login_required
def ajouttucking():

   #La modification du mot de passe par l'administrateur.
   if current_user.role!='Admin':
      return redirect(url_for('main.dashboard'))

   #Titre
   title='Trucking [ Ethiopian Fret'
   #formulaire

   form=AjouTrucking()
   #Code de tracking number unique
   code_tracking=None
   #Verification de l'existe dans la base des données des informations sur Trucking number
   compteur=0
   while compteur < 1: 
      truck=code_trente_min=Trucking.query.filter_by(tracking_number=trucking_number()).first()
      if truck is None:
         code_tracking=trucking_number()
         break
      else:
         pass
      compteur +=1

   if form.validate_on_submit():
      nv_truck=Trucking(tracking_number=code_tracking,ville_provenance=form.ville.data.capitalize(),
                        provenance=form.provenance.data,
                        destination=form.destination.data,
                        date_envoi=form.date_envoi.data)
      db.session.add(nv_truck)
      db.session.commit()
      session['truck']=nv_truck.id
      return redirect(url_for('trucking.littruck'))

   return render_template('trucking/ajouter.html',  title=title, form=form)


""" Liste des colis en track """

@trucking.route('/lis_colis', methods=['GET', 'POST'])
@login_required
def littruck():
   #Titre
   title='Trucking number [ Ethiopian Fret'
   #Requête d'affichage des trucking number
   listes=Trucking.query.order_by(Trucking.id.desc())
   return render_template('trucking/views.html',title=title, liste=listes)

""" Liste des types """

@trucking.route('/lis_devis', methods=['GET', 'POST'])
@login_required
def devis():
   #Titre
   title='Devis | Ethiopian Fret'
   #Requête d'affichage des trucking number
   listes=Devis.query.order_by(Devis.id.desc())
   return render_template('trucking/fret.html',title=title, liste=listes)

""" Ajouter d'une transit """

@trucking.route('/transit_<int:transit_id>_colis', methods=['GET', 'POST'])
@login_required
def ajoutransit(transit_id):
       
   form=TransitTrucking()
   #Titre
   title='Transit [ Ethiopian Fret'
   #Requête de vérification du tracking
   truking_req=Trucking.query.filter_by(id=transit_id).first_or_404()
   #Le nom du type encours de modification
   cate_nom=truking_req.tracking_number
   #Verification de l'existence tracking number
   if truking_req is None:
      return redirect(url_for('trucking.littruck'))
   
   if form.validate_on_submit(): 
      transit=Transit(en_transit=form.en_transit.data, ville_transit=form.ville.data, 
                        date_envoi_transit=form.date_envoi.data, resume=form.resume.data, trucking_id=transit_id)
      db.session.add(transit)
      db.session.commit()
      return redirect(url_for('trucking.littruck'))

   return render_template('trucking/transit.html', form=form, title=title, cate_nom=cate_nom)


""" Livraison du colis"""

@trucking.route('/statut_transit/<int:transit_id>', methods=['GET', 'POST'])
@login_required
def statutranist(transit_id):
   #Titre
   title='Statut Tracking [ Ethiopian Fret'

   #Requête de vérification du trancking
   track_statu=Trucking.query.filter_by(id=transit_id).first_or_404()

   if track_statu is None:
      return redirect(url_for('trucking.littruck'))

   if track_statu.statut == True:
      track_statu.statut=False
      db.session.commit()
      flash("Le colis recommence la route",'success')
      return redirect(url_for('trucking.datelivraison', transit_id=transit_id))
   else:
      track_statu.statut=True
      db.session.commit()
      flash("Le colis est livré",'success')
      return redirect(url_for('trucking.datelivraison', transit_id=transit_id))
   
   return render_template('user/views.html',title=title)

@trucking.route('/encours_transit/<int:transit_id>', methods=['GET', 'POST'])
@login_required
def encours(transit_id):
   #Titre
   title='Statut Tracking [ Ethiopian Fret'

   #Requête de vérification du trancking
   track_statu=Trucking.query.filter_by(id=transit_id).first_or_404()

   if track_statu is None:
      return redirect(url_for('trucking.littruck'))

   if track_statu.encours == True:
      track_statu.encours=False
      db.session.commit()
      flash("Dossier encours de traitement",'success')
      return redirect(url_for('trucking.littruck'))
   else:
      track_statu.encours=True
      db.session.commit()
      flash("Dossier encours de traitement",'success')
      return redirect(url_for('trucking.littruck'))
   
   return render_template('user/views.html',title=title)

@trucking.route('/date_livraison/<int:transit_id>', methods=['GET', 'POST'])
@login_required
def datelivraison(transit_id):
   #Titre
   title='Livarsion colis [ Ethiopian Fret'

   #Requête de vérification du trancking
   track_statu=Trucking.query.filter_by(id=transit_id).first_or_404()

   if track_statu is None:
      return redirect(url_for('trucking.littruck'))

   form=Datelivraison()

   if form.validate_on_submit():
      if track_statu.date_livraison is None and track_statu.statut==True :
         track_statu.date_livraison=form.date_livraison.data
         db.session.commit()
         flash("Le colis est livré", "success")
         return redirect(url_for('trucking.littruck'))
   
   num_track=track_statu.tracking_number
   
   return render_template('trucking/date.html',title=title, truck=num_track, form=form)


@trucking.route('/borderau/<int:transit_id>', methods=['GET', 'POST'])
@login_required
def bordtransit(transit_id):
   #Titre
   title='Bordereaux [ Ethiopian Fret'

   #Requête de vérification du trancking
   track_statu=Trucking.query.filter_by(id=transit_id).first_or_404()
   #Transit du colis.
   track_transit=Transit.query.filter_by(trucking_id=track_statu.id).all()

   if track_statu is None:
      return redirect(url_for('trucking.littruck'))

   return render_template('trucking/document.html',title=title, truck=track_statu, track_transit=track_transit)


""" Modification du trucking  """

@trucking.route('/truckind_<int:transit_id>.kivu', methods=['GET', 'POST'])
@login_required
def trackdocmod(transit_id):
        
   form=MofTrucking()
   #Titre
   title='Modifier bordeaux [ Ethiopian Fret'
   #Requête de vérification du trancking
   track_statu=Trucking.query.filter_by(id=transit_id).first_or_404()
   #Le nom du type encours de modification
   trucking_number_form=track_statu.tracking_number

   if track_statu is None:
      return redirect(url_for('trucking.littruck'))
   
   if form.validate_on_submit():
      track_statu.provenance=form.provenance.data
      track_statu.destination=form.destination.data
      track_statu.ville_provenance=form.ville.data
      db.session.commit()
      flash("Modification réussie",'success')
      return redirect(url_for('trucking.littruck'))
      
   if request.method=='GET':
      form.provenance.data=track_statu.provenance
      form.destination.data=track_statu.destination
      form.ville.data=track_statu.ville_provenance
      form.truckingnumber.data=trucking_number_form

   return render_template('trucking/modform.html', form=form, title=title)



@trucking.route('/trucktranist_<int:transit_id>.kivu', methods=['GET', 'POST'])
@login_required
def tracktransit(transit_id):
       
 
   form=TransitModTrucking()
   #Titre
   title='Modifier bordeaux [ Ethiopian Fret'
   #Requête de vérification du trancking
   track_statu=Transit.query.filter_by(trucking_id=transit_id).first_or_404()


   if track_statu is None:
      return redirect(url_for('trucking.littruck'))
   
   if form.validate_on_submit():
      track_statu.en_transit=form.en_transit.data
      track_statu.ville_transit=form.ville.data
      track_statu.resume=form.resume.data
      db.session.commit()
      flash("Modification réussie",'success')
      return redirect(url_for('trucking.littruck'))
      
   if request.method=='GET':
      form.en_transit.data=track_statu.en_transit
      form.ville.data=track_statu.ville_transit
      form.resume.data=track_statu.resume
      form.truckingnumber.data=track_statu.trucking_transit.tracking_number

   return render_template('trucking/modtransit.html', form=form, title=title)



