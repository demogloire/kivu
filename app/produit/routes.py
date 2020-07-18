from flask import render_template, flash, url_for, redirect, request, session
from .. import db, bcrypt
from ..models import Types, Categorie, Produit
from app.produit.forms import AjoutProForm, AjoutPhoForm, EdProForm,EdPhoForm
from flask_login import login_user, current_user, logout_user, login_required
import app.pack_fonction.fonction as utilitaire
from sqlalchemy.sql import func
from cloudinary.uploader import upload
from cloudinary.utils import cloudinary_url

from . import produit



''' Ajoute un produit '''

@produit.route('/ajout_produit', methods=['GET', 'POST'])
@login_required
def ajoutprod():

   #La modification du mot de passe par l'administrateur.
   if current_user.role!='Admin':
      return redirect(url_for('main.dashboard'))

   #Titre
   title='Produit | Kivu Exchange'
   #formulaire
   form=AjoutProForm()

   if form.validate_on_submit():
      nom_pro=form.nom.data.capitalize()
      #Requete de verification du produit
      req_ver=Produit.query.filter_by(nom=nom_pro, categorie_id=form.rech_cate.data.id).first()
      #Vérification.
      if req_ver is not None:
         flash("Ce produit existe",'success')
         return redirect(url_for('produit.ajoutprod')) 
      #Code du produit
      code_produit_une=db.session.query(func.max(Produit.id).label("idmax")).first()
      code_pro_systeme=""
      if code_produit_une.idmax is None:
         code_pro_systeme="#{}1".format(form.rech_cate.data.id)
      else:
         precede_prod=code_produit_une.idmax + 1
         if precede_prod < 10:
               precede_prod="{}{}".format(0,precede_prod)
               code_pro_systeme="#{}{}".format(form.rech_cate.data.id,precede_prod)
         else:
               code_pro_systeme="#{}{}".format(form.rech_cate.data.id,precede_prod)
      
      #Code unique
      code_produit=code_pro_systeme
      #Produit 
      if form.img_url.data=="":
         produit_enre=Produit(nom=nom_pro, mesure=form.mesure.data, description=form.resume.data, description_android=form.resume_android.data, categorie_id=form.rech_cate.data.id, prix_p=form.prix_p.data,user_produit=current_user, statut=False, code=code_produit)
         db.session.add(produit_enre)
         db.session.commit()
         flash("Charger l'image du produit maintenant!",'success')
         session['img']=code_produit
         return redirect(url_for('produit.upload_file'))
      else: 
         produit_enre=Produit(nom=nom_pro, mesure=form.mesure.data, description=form.resume.data, description_android=form.resume_android.data, categorie_id=form.rech_cate.data.id, prix_p=form.prix_p.data,user_produit=current_user, img_url=form.img_url.data, statut=False, code=code_produit)
         db.session.add(produit_enre)
         db.session.commit()
         flash("Ajout d'un nouveau produit",'success')
      return redirect(url_for('produit.lipro')) 

   return render_template('produit/ajpro.html',  title=title, form=form)

""" Liste des produits """

@produit.route('/lis_produit', methods=['GET', 'POST'])
@login_required
def lipro():
   
   #La modification du mot de passe par l'administrateur.
   if current_user.role!='Admin':
      return redirect(url_for('main.dashboard'))
   #Titre
   title='Produit | Kivu Exchange'
   #Requet des pagination et des listage des données
   page= request.args.get('page', 1, type=int)
   livre_page=Produit.query.order_by(Produit.id.desc()).paginate(page=page, per_page=50)
    
   return render_template('produit/views.html', title=title, liste=livre_page)


""" Upload l'image avec Cloudinary """

@produit.route('/img', methods=['GET', 'POST'])
def upload_file():
   
   #Titre
   title="Image | Kivu Exchanges"
   #Verification de session
   if 'img' in session:
      id_rech=session['img']
   else:
      return redirect(url_for('produit.ajoutprod')) 
   #Produit à modifier
   prod_img=Produit.query.filter_by(code=id_rech).first() 
   #Formualire
   form=AjoutPhoForm()
   upload_result = None
   if form.validate_on_submit():
      file_to_upload = form.file.data
      if file_to_upload:
         upload_result = utilitaire.save_picture(file_to_upload)
         prod_img.img_url=upload_result
         db.session.commit()
         flash("Ajout d'un nouveau produit",'success')
         session.pop('img',None)
         return redirect(url_for('produit.lipro')) 
   return render_template('produit/upload_form.html', form=form)


""" Modifier statut du produit"""

@produit.route('/statut_produit/<int:pro_id>', methods=['GET', 'POST'])
@login_required
def statutpro(pro_id):
   #Titre
   title='Produit | Kivu Exchanges'

   #verification de l'administrateur.
   if current_user.role!='Admin':
      return redirect(url_for('main.dashboard'))

   #Requête de vérification de produit
   pro_statu=Produit.query.filter_by(id=pro_id).first()

   if pro_statu is None:
      return redirect(url_for('produit.lipro'))

   if pro_statu.statut == True:
      pro_statu.statut=False
      db.session.commit()
      flash("Le produit est activé sur la plateforme",'success')
      return redirect(url_for('produit.lipro'))
   else:
      pro_statu.statut=True
      db.session.commit()
      flash("Le produit est desactivé sur la plateforme",'success')
      return redirect(url_for('produit.lipro'))
   
   return render_template('user/views.html',title=title)


""" Modification du produit  """

@produit.route('/edit_<int:pro_id>_pro', methods=['GET', 'POST'])
@login_required
def editpro(pro_id):
       
   #Modification par l'administrateur
   if current_user.role!='Admin':
      return redirect(url_for('main.dashboard'))       
   
   form=EdProForm()
   #Titre
   title='Produit | Kivu Exchange'
   #Requête de vérification du type
   pro_class=Produit.query.filter_by(id=pro_id).first()
   #Le nom du type encours de modification
   pro_nom=pro_class.nom

   if pro_class is None:
      return redirect(url_for('produit.litcate'))
   
   if form.validate_on_submit():
      req_ver=Produit.query.filter_by(nom=form.ed_nom.data.capitalize(), categorie_id=form.ed_rech_cate.data.id).first()
      
      if req_ver is None:
         if form.ed_img_url.data=="":
            pro_class.nom=form.ed_nom.data.capitalize()
            pro_class.categorie_id=form.ed_rech_cate.data.id
            pro_class.prix_p=form.ed_prix_p.data
            pro_class.resume_android=form.resume_android.data
            pro_class.description=form.resume.data
            pro_class.mesure=form.mesure.data
            db.session.commit()
            flash("Veuillez upload l'image",'success')
            session['img']=pro_id
            return redirect(url_for('produit.upload_file_ed', pro_id=pro_id))
         else:
            pro_class.nom=form.ed_nom.data.capitalize()
            pro_class.categorie_id=form.ed_rech_cate.data.id
            pro_class.prix_p=form.ed_prix_p.data
            pro_class.img_url=form.ed_img_url.data
            pro_class.description=form.resume.data
            pro_class.resume_android=form.resume_android.data
            pro_class.mesure=form.mesure.data
            db.session.commit()
            flash("Modification réussie",'success')
            return redirect(url_for('produit.lipro'))
            
      else:
         if form.ed_img_url.data=="":
            pro_class.prix_p=form.ed_prix_p.data
            pro_class.description=form.resume.data
            pro_class.resume_android=form.resume_android.data
            pro_class.mesure=form.mesure.data
            db.session.commit()
            flash("Veuillez upload l'image",'success')
            session['img']=pro_id
            return redirect(url_for('produit.upload_file_ed', pro_id=pro_id))
         else:
            pro_class.prix_p=form.ed_prix_p.data
            pro_class.img_url=form.ed_img_url.data
            pro_class.description=form.resume.data
            pro_class.resume_android=form.resume_android.data
            pro_class.mesure=form.mesure.data
            db.session.commit()
            flash("Modification réussie",'success')
            return redirect(url_for('produit.litcate'))

   if request.method=='GET':
      form.ed_nom.data=pro_class.nom
      form.ed_rech_cate.data=pro_class.categorie_produit.nom
      form.ed_prix_p.data=pro_class.prix_p
      form.ed_img_url.data=pro_class.img_url
      form.resume.data=pro_class.description
      form.resume_android.data=pro_class.resume_android
      form.mesure.data=pro_class.mesure
   return render_template('produit/editpro.html', form=form, title=title, pro_nom=pro_nom)


""" Upload l'image avec Cloudinary """

@produit.route('/imged<int:pro_id>', methods=['GET', 'POST'])
def upload_file_ed(pro_id):
   
   #Titre
   title="Image | Kivu Exchanges"
   #Verification de session
   if 'img' in session:
      id_rech=session['img']
   else:
      return redirect(url_for('produit.lipro')) 
   #Produit à modifier
   prod_img=Produit.query.filter_by(id=pro_id).first() 
   #Formualire
   form=EdPhoForm()
   upload_result = None
   if form.validate_on_submit():
      file_to_upload = form.ed_file.data
      if file_to_upload:
         upload_result = utilitaire.save_picture(file_to_upload)
         prod_img.img_url=upload_result
         db.session.commit()
         flash("Modification avec succès",'success')
         session.pop('img',None)
         return redirect(url_for('produit.lipro')) 
   return render_template('produit/upload_form_ed.html', form=form, title=title)