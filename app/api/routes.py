import os
import json
from flask import jsonify, request, make_response
from .. import db, bcrypt
from ..models import User, Produit, ProduitSchema, UserSchema, Commandes, CommandesSchema, Facture, Panier, FactureSchema, PanierSchema, Categorie, CategorieSchema 
from flask_restful import Resource, Api
import uuid
import jwt
import datetime
from functools import wraps
from app.api.function_api import token_required, codecommande, DecimalEncoder, produit_du_panier

#from flask_login import login_user, current_user, logout_user, login_required
from . import apis
from app import create_app

config_name = os.getenv('FLASK_CONFIG')
app = create_app(config_name)




#Enregistrement des utilisateurs
@apis.route('/utilisateur',methods=['POST'])
def ajouterutilisateur():
    """ Cette fonction enregistre l'utilisateur en passant les données de:
       nom, post_nom, prenom, password, username, téléphone,  mail, adresse physique.
       Avec un contrôle sur username qui est unique si username existe déjà, elle retroune 
       variable de contrôle control_process: False, Sinon elle enregistre le client avec
       retournant dans la variable de controle control_process: True 
    """

    data=request.get_json()

    password_hash=bcrypt.generate_password_hash(data['password']).decode('utf-8')  
    verifcation_user=User.query.filter_by(username=data['username']).first()
    #Enregistrement d'un client sur API
    if verifcation_user is None:
        utilisateur=User(public_id=str(uuid.uuid4()), nom=data['nom'], prenom=data['prenom'],post_nom=data['post_nom'], password=password_hash, username=data['username'],role='Client', 
                        tel=data['tel'], mail=data['mail'], adr=data['adr'], statut=True)
        db.session.add(utilisateur)
        db.session.commit()
        return jsonify({'message':'success',"control_process":True})
    else:
        return jsonify({'message':'attention',"control_process":False})
    return jsonify({'message':'success'})


#Profil de l'utilisateur
@apis.route('/profil',methods=['GET'])
@token_required
def profil(current_user):
    user=User.query.filter_by(id=current_user.id).first()
    user_one=[]
    nbre_panier=produit_du_panier()
    utilisateur_donnees={
        "nom": user.nom,
        "post_nom":user.post_nom,
        "prenom":user.prenom,
        "tel":user.tel,
        "mail":user.mail,
        "adr":user.adr,
        "username":user.username
    }
    user_one.insert(0,utilisateur_donnees)
    return jsonify({'message':'success', "utilisateur":user_one, 'nbre_panier':nbre_panier})

#Mise à jour du profil
@apis.route('/maj/profil',methods=['GET','PUT'])
@token_required
def profil_maj(current_user):
    user=User.query.filter_by(id=current_user.id).first()
    # Les données du formulaire
    data=request.get_json()
    nbre_panier=produit_du_panier()
    user_one=[]
    utilisateur_donnees={
        "nom": user.nom,
        "post_nom":user.post_nom,
        "prenom":user.prenom,
        "tel":user.tel,
        "mail":user.mail,
        "adr":user.adr,
        "username":user.username
    }
    user_one.insert(0,utilisateur_donnees)
    if data is not None:
        user_name=User.query.filter_by(username=data['username']).first()
        if user_name:
            user.nom=data['nom']
            user.post_nom=data['post_nom']
            user.prenom=data['prenom']
            user.tel=data['tel']
            user.mail=data['mail']
            user.adr=data['adr']
            db.session.commit()
            return jsonify({'message':'Mise à jour avec succès', "control_process":True })
        else:
            user.nom=data['nom']
            user.post_nom=data['post_nom']
            user.prenom=data['prenom']
            user.tel=data['tel']
            user.mail=data['mail']
            user.adr=data['adr']
            user.username=data['username']
            db.session.commit()
            return jsonify({'message':'Mise à jour avec succès', "control_process":True })
    return jsonify({'message':'Envoie les données svp','utili_donnees': user_one, 'nbre_panier':nbre_panier})

#Enregistrement des utilisateurs
@apis.route('/majpass/profil',methods=['GET','PUT'])
@token_required
def profil_pass(current_user):
    user=User.query.filter_by(id=current_user.id).first()
    # Les données du formulaire
    data=request.get_json()
    user_one=[]
    nbre_panier=produit_du_panier()
    utilisateur_donnees={
        "nom": user.nom,
        "post_nom":user.post_nom,
        "prenom":user.prenom,
        "tel":user.tel,
        "mail":user.mail,
        "adr":user.adr,
        "username":user.username
    }
    user_one.insert(0,utilisateur_donnees)
    if data is not None:
        password_hash=bcrypt.generate_password_hash(data['password']).decode('utf-8')
        user.password=password_hash
        db.session.commit()  
        return jsonify({'message':'Mise à jour avec succès', "control_process":True })
        
    return jsonify({'message':'Envoie les données svp','utili_donnees': user_one, 'nbre_panier':nbre_panier})


#Liste des produits en exposition
@apis.route('/produit',methods=['GET'])
@token_required
def produit(current_user):
    """ Cette fonction retourne la liste des produits en expositions """
    produit_schema = ProduitSchema()
    produits_schema = ProduitSchema(many=True)
    produit_all=produits_schema.dump(Produit.query.filter_by(statut=True).all()) 
    #Les produits en de la catélogues
    tous_les_produit=Produit.query.filter_by(statut=True).all()
    #Liste des produits
    produits=[]

    nbre_panier=produit_du_panier()

    for produit in tous_les_produit:
        p={
            'id': produit.id,
            'nom': produit.nom,
            'prix_p':produit.prix_p,
            'code':produit.code,
            'img_url':produit.img_url,
            'description_android':produit.description_android,
            'mesure': produit.mesure,
            'categori_id':produit.categorie_produit.id,
            'nom_categorie':produit.categorie_produit.nom,
        }
        produits.insert(0,p)

    return jsonify({'produits':produits,'nbre_panier':nbre_panier})


#utilisateur encours d'utilisation
@apis.route('/utilisateur',methods=['GET'])
@token_required
def utilisateur(current_user):
    """ Cette fonction retourne un utilisateur la variable utilisateurs un_utilisateur
        dans le cas contraire elle retourne une erreur avec la variable de contrôle
        control_process: False
    """
    nbre_panier=produit_du_panier()
    user_schema = UserSchema()
    users_schema = UserSchema(many=True)
    verifcation_user_profil=User.query.filter_by(id=current_user.id).first()
    if verifcation_user_profil is None :
        return jsonify({'message':"Aucun utilisateur associer","control_process":False})
    user_one=user_schema.dump(verifcation_user_profil) 
    return jsonify({'un_utilisateur':user_one,'nbre_panier':nbre_panier})


#Ajout au panier
@apis.route('/produit_panier/<int:id>',methods=['POST','GET','PUT'])
@token_required
def produit_vente(current_user, id):
    """ Cette fonction retourne une variable control_process: True en cas de réussité du processus
        dans le cas contraire False
    """
    data=request.get_json()

    if not id:
        return jsonify({'message':"Vérifier les parametres","control_process":False})

    produit_schema = ProduitSchema()
    produits_schema = ProduitSchema(many=True)
    #Le nombre des produits dans le panier
    nbre_panier=produit_du_panier()

    verifcation_porduit_vente=Produit.query.filter_by(id=id).first()
    if verifcation_porduit_vente is None :
        return jsonify({'message':"Ce produit n'existe pas","control_process":False,'nbre_panier':nbre_panier})
    else:
        commande_ajout=Commandes.query.filter_by(user_id=current_user.id, produit_id=id).first()
        if commande_ajout is None:
            valeur_commande= float(data['qte']) * float(verifcation_porduit_vente.prix_p)
            enregistrement_commande=Commandes(prix_p=verifcation_porduit_vente.prix_p,qte=data['qte'], somme=valeur_commande, user_id=current_user.id, produit_id=id)
            db.session.add(enregistrement_commande)
            db.session.commit()
            return jsonify({'message':"Ajout au panier avec succès","control_process":True,'nbre_panier':nbre_panier})
        else:
            valeur_commande_entree= float(data['qte']) * float(verifcation_porduit_vente.prix_p)
            qte_nouvelle = data['qte']
            valeur_commande_nouvelle= valeur_commande_entree 
            commande_ajout.qte=qte_nouvelle
            commande_ajout.somme=valeur_commande_nouvelle
            db.session.commit()
            return jsonify({'message':"Ajout au panier avec succès","control_process":True,'nbre_panier':nbre_panier})
    return jsonify({'message':'Verifier les information',"control_process":False,'nbre_panier':nbre_panier})


#Ajout au panier
@apis.route('/produit_supprimer/<int:id>',methods=['DELETE'])
@token_required
def produit_suprimer(current_user, id):
    """ Cette fonction retourne une variable control_process: True en cas de réussité du processus
        dans le cas contraire
    """
    #Le nombre des produits dans le panier
    nbre_panier=produit_du_panier()

    if not id:
        return jsonify({'message':"Vérifier les parametres","control_process":False,'nbre_panier':nbre_panier})
    verifcation_porduit_vente=Produit.query.filter_by(id=id).first()
    if verifcation_porduit_vente is None :
        return jsonify({'message':"Ce produit n'existe pas","control_process":False,'nbre_panier':nbre_panier})
    else:
        commande_ajout=Commandes.query.filter_by(user_id=current_user.id, produit_id=id).delete()
        db.session.commit()
        return jsonify({'message':"Suppression avec success","control_process":True,'nbre_panier':nbre_panier})
    return jsonify({'message':'Verifier les information',"control_process":False,'nbre_panier':nbre_panier })

#Diminution de la vente
@apis.route('/produit_panier_moins/<int:id>',methods=['POST','GET','PUT'])
@token_required
def produit_vente_moins(current_user, id):
    """ Cette fonction retourne une variable control_process: True en cas de réussité du processus
        dans le cas contraire
    """
    data=request.get_json()

    #Le nombre des produits dans le panier
    nbre_panier=produit_du_panier()

    if not id:
        return jsonify({'message':"Vérifier les parametres","control_process":False,'nbre_panier':nbre_panier})

    produi_schema = ProduitSchema()
    produits_schema = ProduitSchema(many=True)

    verifcation_porduit_vente=Produit.query.filter_by(id=id).first()
    if verifcation_porduit_vente is None :
        return jsonify({'message':"Ce produit n'existe pas","control_process":False,'nbre_panier':nbre_panier})
    else:
        commande_ajout=Commandes.query.filter_by(user_id=current_user.id, produit_id=id).first()
        if commande_ajout is None:
            valeur_commande= float(data['qte']) * float(verifcation_porduit_vente.prix_p)
            enregistrement_commande=Commandes(qte=data['qte'], somme=valeur_commande, user_id=current_user.id, produit_id=id)
            db.session.add(enregistrement_commande)
            db.session.commit()
            return jsonify({'message':"Ajout au panier avec succès","control_process":True,'nbre_panier':nbre_panier})
        else:
            valeur_commande_entree= float(data['qte']) * float(verifcation_porduit_vente.prix_p)
            if commande_ajout.qte > data['qte'] :
                qte_nouvelle = commande_ajout.qte - data['qte']
                valeur_commande_noubelle= valeur_commande_entree + float(commande_ajout.somme) 
                commande_ajout.qte=qte_nouvelle
                commande_ajout.somme=valeur_commande_noubelle
                db.session.commit()
                return jsonify({'message':"Diminution au panier avec succès","control_process":True,'nbre_panier':nbre_panier})
            else:
                return jsonify({'message':'La quantité est superieur à la quantité disponible',"control_process":False,'nbre_panier':nbre_panier })
    return jsonify({'message':'Verifier les information',"control_process":False,'nbre_panier':nbre_panier })


#Liste le panier des produits
@apis.route('/panier',methods=['GET'])
@token_required
def panier(current_user):
    """ Cette fonction retourne le panier du client avec la veleur totale de l'utilisateur """
    valeur_produit_panier=[]
    panier=[]
    nombre_panier=[]

    commandes_schema = CommandesSchema(many=True)
    commandes_client=Commandes.query.filter_by(user_id=current_user.id).all()
    #Ajout des elements dans le panier
    for p in commandes_client:
        p={
            'id': p.produit_commande.id,
            'nom_produit': p.produit_commande.nom,
			'url_image':  p.produit_commande.img_url,
			'categorie' : p.produit_commande.categorie_produit.nom,
			'qte': float(p.qte),
			'somme': float(p.somme),
        }
        panier.insert(0,p)
    #Nom
    nbr_produit_panier=len(panier)
    nbr_produit_panier=nbr_produit_panier

    if commandes_client==[]:
        return jsonify({'message':'Aucun produit dans le panier',"control_process":False})
    for commande_valeur in commandes_client:
      i=float(commande_valeur.somme)
      valeur_produit_panier.insert(0,i)
    #Panier et le nombre d'element du panier
    valeur_totale=sum(valeur_produit_panier)
    valeur_totale=valeur_totale
    panier_produit=panier
    
    return jsonify({'panier':panier_produit, 'valeur':valeur_totale,"control_process":True, 'nbre_panier':nbr_produit_panier })



#Liste commandé produit
@apis.route('/commander',methods=['POST','GET','DELETE','PUT'])
@token_required
def commander(current_user):

    #Le nombre des produits dans le panier
    nbre_panier=produit_du_panier()
    """ Cette fonction retourne la variable control_process en True, si la commande a reussi et False si vous n'avez rien dans le panier """
    valeur_produit_panier=[]
    commandes_schema = CommandesSchema(many=True)
    commandes_client=Commandes.query.filter_by(user_id=current_user.id).all()
    if commandes_client==[]:
        return jsonify({'message':'Aucun produit dans le panier',"control_process":False,'nbre_panier':nbre_panier})

    code_encours=codecommande() #Code de la facture
    valeur_commande_panier=[]
    
    enre_facture=Facture(code_commande=code_encours, user_id=current_user.id)
    db.session.add(enre_facture)
    db.session.commit()

    for dans_commande_panier in commandes_client:
        #Enregistrement dans le panier
        valeur_total_panier=float(dans_commande_panier.qte) * float(dans_commande_panier.produit_commande.prix_p)
        vente_encours=Panier(quantite=dans_commande_panier.qte, prix_p=dans_commande_panier.produit_commande.prix_p, valeur=valeur_total_panier,
                                user_id=current_user.id, produit_id=dans_commande_panier.produit_id, facture_id=enre_facture.id)
        db.session.add(vente_encours)
        #Facture encours d'enregistrement
        enre_facture_montant=Facture.query.filter_by(id=enre_facture.id).first()
        if enre_facture_montant.valeur is None:
            enre_facture_montant.valeur=valeur_total_panier
        else:
            enre_facture_montant.valeur= float(enre_facture_montant.valeur) + valeur_total_panier
        Commandes.query.filter_by(id=dans_commande_panier.id).delete()
        db.session.commit()

    return jsonify({'message':"Commande reussie", "control_process":True,'nbre_panier':nbre_panier })


#Liste commandé produit
@apis.route('/commandes/<int:id>',methods=['GET'])
@token_required
def commande_utilisateur(current_user, id):
    """ Cette fonction retourne liste des produit du panier, la valeur totale du panier et control_process True dans le cas 
    contraire control_procesd est False """

    enre_facture_montant=Facture.query.filter_by(id=id).first()

    panier=[]

    #Le nombre des produits dans le panier
    nbre_panier=produit_du_panier()

    if enre_facture_montant is None:
        return jsonify({'message':"Cette commande n'existe pas","control_process":False,'nbre_panier':nbre_panier})

    panier_des_donnes=Panier.query.filter_by(facture_id=id).all()
    if panier_des_donnes==[]:
        return jsonify({'message':"Aucun produit dans la commande","control_process":False,'nbre_panier':nbre_panier})
    #Valeur total de la commande
    val_com_facture=[]
    for  paniers in panier_des_donnes:
        i=paniers.valeur
        val_com_facture.insert(0,i)
    valeur_totale_panier=sum(val_com_facture)

    #Ajout des elements dans le panier
    for p in panier_des_donnes:
        p={
            'id': p.produit_panier.id,
            'nom_produit': p.produit_panier.nom,
			'url_image':  p.produit_panier.img_url,
			'categorie' : p.produit_panier.categorie_produit.nom,
			'qte': int(p.quantite),
            'prix_p':float(p.prix_p),
			'somme': float(p.valeur),
        }
        panier.insert(0,p)
    #Nom
    nbr_produit_panier=len(panier)
    nbr_produit_panier=nbr_produit_panier
    commande_pan=panier
    nbre_commande=len(panier)

    return jsonify({'message':'Produit de commande','nbre_commande':nbre_commande,'commande':commande_pan,"valeur_panier":valeur_totale_panier,"control_process":True,'nbre_panier':nbre_panier })


#Liste des produits en exposition
@apis.route('/commandes',methods=['GET'])
@token_required
def commandes(current_user):
    """ Cette fonction retourne la liste des commandes"""
    commdandes_encours=[]
    commande=Facture.query.filter_by(user_id=current_user.id).all()
    if commande == []:
        return jsonify({'message':"Aucune commande disponible","control_process":False})
    
    for com in commande:
        p={
            "adr":  com.adr,
            "annul": com.annul,
            "code_commande": com.code_commande,
            "datecommande": com.datecommande,
            "deuxieme_payement": com.deuxieme_payement,
            "id": com.id,
            "mail": com.mail,
            "paniers": [{'id' : i.id, 'nom_produit': i.produit_panier.nom, 'url_image':  i.produit_panier.img_url, 'mesure' : i.produit_panier.mesure, "qte":i.quantite, "valeur":i.valeur, 'prix_p':i.prix_p }  for i in com.paniers],
            "premier_payement": com.premier_payement,
            "ref_payement_deux": com.ref_payement_deux,
            "ref_payement_totalite": com.ref_payement_totalite,
            "ref_payement_un": com.ref_payement_un,
            "statut": com.statut,
            "tel": com.tel,
            "totalite": com.totalite,
            "valeur": com.valeur
        }
        commdandes_encours.insert(0,p)
        
    
    #Le nombre des produits dans le panier
    commdandes_encours_nbr=len(commdandes_encours)
    nbre_panier=produit_du_panier()
    return jsonify({'commandes':commdandes_encours,'nbr_commande':commdandes_encours_nbr,  'message':"Liste des commandes","control_process":True,'nbre_panier':nbre_panier})


#Liste des categories
@apis.route('/categories',methods=['GET'])
@token_required
def categorie(current_user):
    """ Cette fonction retourne la liste des commandes"""
    #Le nombre des produits dans le panier
    nbre_panier=produit_du_panier()

    categorie_de_produit=[]
    categories=Categorie.query.filter_by(statut=True).order_by(Categorie.id.desc()).all()
    if categories == []:
        return jsonify({'message':"Aucune categorie n'est disponible","control_process":False,'nbre_panier':nbre_panier})
    
    for cat in categories:
        categ = {'id':cat.id,'nom':cat.nom, 'produit':[{'id' : i.id, 'nom_produit': i.nom, 'url_image':  i.img_url, 'mesure' : i.mesure, 'prix_p':i.prix_p }  for i in cat.produits]}
        #categ=json.dumps(categ, cls=DecimalEncoder)
        categorie_de_produit.insert(0,categ)
       
    return jsonify({'categorie':categorie_de_produit,'message':"Listes des categories","control_process":True,'nbre_panier':nbre_panier})

#Liste des produits en exposition
@apis.route('/categories/<int:id>',methods=['GET'])
@token_required
def categorie_produit(current_user, id):
    """ Cette fonction retourne la liste des commandes"""
    #Le nombre des produits dans le panier
    nbre_panier=produit_du_panier()

    categories=Categorie.query.filter_by(id=id).first()
    if categories is None:
        return jsonify({'message':"Aucune categorie n'est disponible","control_process":False,'nbre_panier':nbre_panier})

    produit_categorie=Produit.query.filter_by(statut=True, categorie_id=id).all()
    produits_schema = ProduitSchema(many=True)
    produits_categorie=produits_schema.dump(produit_categorie) 
    return jsonify({'produits':produits_categorie,'message':"Liste des produit par catégorie","control_process":True,'nbre_panier':nbre_panier})

#Payements
@apis.route('/payement/<int:id>',methods=['GET','PUT'])
@token_required
def payements(current_user, id):
    """ Pyament de commandes"""
    #Le nombre des produits dans le panier
    nbre_panier=produit_du_panier()
    #Les données du formulaire
    data=request.get_json()
    #La facture
    facture_encours=Facture.query.filter_by(id=id, user_id=current_user.id).first()
    if facture_encours.premier_payement == 0 or facture_encours.premier_payement is None  and facture_encours.totalite==False:
        #Payements
        produit_facture=[]
        panier_de_facture=Panier.query.filter_by(facture_id=id, user_id=current_user.id).all()
        for produit in panier_de_facture:
            p={
                'id':produit.produit_panier.id,
                'nom_produit':produit.produit_panier.nom,
                'img_url':produit.produit_panier.img_url,
                'quantite':produit.quantite,
                'prix_p':produit.prix_p,
                'valeur':produit.valeur
            }
            produit_facture.insert(0,p)
        #Les informations de la factures
        
        if data is not None:
            if data['premier_payement']==facture_encours.valeur:
                facture_encours.ref_payement_un= data['ref_payement_un']
                facture_encours.totalite=True
                facture_encours.tel=data['tel']
                facture_encours.mail=data['mail']
                facture_encours.adr=data['adr']
            else:
                facture_encours.premier_payement=data['premier_payement']
                facture_encours.ref_payement_un=data['ref_payement_un']
                facture_encours.tel=data['tel']
                facture_encours.mail=data['mail']
                facture_encours.adr=data['adr']
            db.session.commit()
            return jsonify({'produit':produit_facture,'message':"Premier payement effectué","control_process":True,'nbre_panier':nbre_panier})
        
        #Valeur de la panier 
        
    else:
        #Payements
        produit_facture=[]
        panier_de_facture=Panier.query.filter_by(facture_id=id, user_id=current_user.id).all()
        for produit in panier_de_facture:
            p={
                'id':produit.produit_panier.id,
                'nom_produit':produit.produit_panier.nom,
                'img_url':produit.produit_panier.img_url,
                'quantite':produit.quantite,
                'prix_p':produit.prix_p,
                'valeur':produit.valeur
            }
            produit_facture.insert(0,p)

        return jsonify({'produit':produit_facture,'message':"Effectué le deuxieme payement",'premier_payement':facture_encours.premier_payement,'total_facture':facture_encours.valeur,"control_process":False,'nbre_panier':nbre_panier})

#Payements
@apis.route('/deux/payement/<int:id>',methods=['GET','PUT'])
@token_required
def payements_deux(current_user, id):
    """ Pyament de commandes"""
    #Le nombre des produits dans le panier
    nbre_panier=produit_du_panier()
    #La facture
    facture_encours=Facture.query.filter_by(id=id, user_id=current_user.id).first()
    if facture_encours.premier_payement != 0 and facture_encours.totalite==False:
        #Les données du formulaire
        data=request.get_json()
        #Payements
        produit_facture=[]
        panier_de_facture=Panier.query.filter_by(facture_id=id, user_id=current_user.id).all()
        for produit in panier_de_facture:
            p={
                'id':produit.produit_panier.id,
                'nom_produit':produit.produit_panier.nom,
                'img_url':produit.produit_panier.img_url,
                'quantite':produit.quantite,
                'prix_p':produit.prix_p,
                'valeur':produit.valeur
            }
            produit_facture.insert(0,p)
        #Vérification des payement
        if data is not None:
            premier=float(facture_encours.premier_payement)
            total=float(facture_encours.valeur)
            payement_deuxieme=float(data['premier_deuxieme'])
            #La difference
            addition = premier + payement_deuxieme
            if addition == total:
                facture_encours.totalite=True
                facture_encours.deuxieme_payement=payement_deuxieme
                facture_encours.ref_payement_deux=data['ref_payement_deux']
                db.session.commit()
                return jsonify({'produit':produit_facture,'message':"Payement éffectué",'premier_payement':facture_encours.premier_payement,'deuxieme_payement':facture_encours.deuxieme_payement,'total_facture':facture_encours.valeur,"control_process":True,'nbre_panier':nbre_panier})
 
            else:
                reste= total - addition
                if reste < 0:
                    #Payements
                    produit_facture=[]
                    panier_de_facture=Panier.query.filter_by(facture_id=id, user_id=current_user.id).all()
                    for produit in panier_de_facture:
                        p={
                            'id':produit.produit_panier.id,
                            'nom_produit':produit.produit_panier.nom,
                            'img_url':produit.produit_panier.img_url,
                            'quantite':produit.quantite,
                            'prix_p':produit.prix_p,
                            'valeur':produit.valeur
                        }
                        produit_facture.insert(0,p)

                    return jsonify({'produit':produit_facture,'message':"Effectué juste le reste",'premier_payement':facture_encours.premier_payement,'total_facture':facture_encours.valeur,"control_process":False,'nbre_panier':nbre_panier})

                if reste > 0:
                    #Payements
                    produit_facture=[]
                    panier_de_facture=Panier.query.filter_by(facture_id=id, user_id=current_user.id).all()
                    for produit in panier_de_facture:
                        p={
                            'id':produit.produit_panier.id,
                            'nom_produit':produit.produit_panier.nom,
                            'img_url':produit.produit_panier.img_url,
                            'quantite':produit.quantite,
                            'prix_p':produit.prix_p,
                            'valeur':produit.valeur
                        }
                        produit_facture.insert(0,p)

                    return jsonify({'produit':produit_facture,'message':"Payer la totalité du reste",'premier_payement':facture_encours.premier_payement,'total_facture':facture_encours.valeur,"control_process":False,'nbre_panier':nbre_panier})
    else:
        #Payements
        produit_facture=[]
        panier_de_facture=Panier.query.filter_by(facture_id=id, user_id=current_user.id).all()
        for produit in panier_de_facture:
            p={
                'id':produit.produit_panier.id,
                'nom_produit':produit.produit_panier.nom,
                'img_url':produit.produit_panier.img_url,
                'quantite':produit.quantite,
                'prix_p':produit.prix_p,
                'valeur':produit.valeur
            }
            produit_facture.insert(0,p)

        return jsonify({'produit':produit_facture,'message':"Effectué le deuxieme payement",'premier_payement':facture_encours.premier_payement,'total_facture':facture_encours.valeur,"control_process":False,'nbre_panier':nbre_panier})

#Connextion à l'api
@apis.route('/login')
@apis.route('/')
def login():
    """" 
    Connexion à la plateforme des vente, elle retourne True de la variable control_process .        
    """
    auth = request.authorization
    if not auth or not auth.username or not auth.password:
        return make_response('Vérifier les identifiants', 401, {'WWW.Authentication': 'Basic realm: "Connectez-vous"'})
    user = User.query.filter_by(username=auth.username).first()

    if not user:
        return make_response('Vérifier les identifiants', 401, {'WWW.Authentication': 'Basic realm: "Connectez-vous"'})

    if bcrypt.check_password_hash(user.password, auth.password):
        token = jwt.encode({'public_id': user.public_id, 'exp' : datetime.datetime.utcnow() + datetime.timedelta(minutes=30)}, app.config['SECRET_KEY'])
        return jsonify({'token' : token.decode('UTF-8'), "control_process":True})
   
    return make_response('Vérifier les identifiants',  401, {'WWW.Authentication': 'Basic realm: "Connectez-vous"'})


