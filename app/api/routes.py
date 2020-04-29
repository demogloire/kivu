import os
from flask import jsonify, request, make_response
from .. import db, bcrypt
from ..models import User, Produit, ProduitSchema, UserSchema, Commandes, CommandesSchema, Facture, Panier, FactureSchema, PanierSchema, Categorie, CategorieSchema 
from flask_restful import Resource, Api
import uuid
import jwt
import datetime
from functools import wraps
from app.api.function_api import token_required, codecommande
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


#Listage des utilisateurs
@apis.route('/utilisateur',methods=['GET'])
@token_required
def lesutilisateur(current_user):
    """ Cette fonction retourne la liste des utilisateurs dans la variable utilisateurs """
    user_schema = UserSchema()
    users_schema = UserSchema(many=True)
    user_all=users_schema.dump(User.query.all()) 
    return jsonify({'utilisateurs':user_all})


#Liste des produits en exposition
@apis.route('/produit',methods=['GET'])
@token_required
def produit(current_user):
    """ Cette fonction retourne la liste des produits en expositions """
    produit_schema = ProduitSchema()
    produits_schema = ProduitSchema(many=True)
    produit_all=produits_schema.dump(Produit.query.filter_by(statut=True).all()) 
    return jsonify({'produits':produit_all})


#utilisateur encours d'utilisation
@apis.route('/utilisateur/<string:public_id>',methods=['GET'])
@token_required
def utilisateur(current_user, public_id):
    """ Cette fonction retourne un utilisateur la variable utilisateurs un_utilisateur
        dans le cas contraire elle retourne une erreur avec la variable de contrôle
        control_process: False
    """
    user_schema = UserSchema()
    users_schema = UserSchema(many=True)
    verifcation_user_profil=User.query.filter_by(public_id=public_id).first()
    if verifcation_user_profil is None :
        return jsonify({'message':"Aucun utilisateur associer","control_process":False})
    user_one=user_schema.dump(verifcation_user_profil) 
    return jsonify({'un_utilisateur':user_one})


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

    verifcation_porduit_vente=Produit.query.filter_by(id=id).first()
    if verifcation_porduit_vente is None :
        return jsonify({'message':"Ce produit n'existe pas","control_process":False})
    else:
        commande_ajout=Commandes.query.filter_by(user_id=current_user.id, produit_id=id).first()
        if commande_ajout is None:
            valeur_commande= float(data['qte']) * float(verifcation_porduit_vente.prix_p)
            enregistrement_commande=Commandes(qte=data['qte'], somme=valeur_commande, user_id=current_user.id, produit_id=id)
            db.session.add(enregistrement_commande)
            db.session.commit()
            return jsonify({'message':"Ajout au panier avec succès","control_process":True})
        else:
            valeur_commande_entree= float(data['qte']) * float(verifcation_porduit_vente.prix_p)
            qte_nouvelle = data['qte']
            valeur_commande_nouvelle= valeur_commande_entree 
            commande_ajout.qte=qte_nouvelle
            commande_ajout.somme=valeur_commande_nouvelle
            db.session.commit()
            return jsonify({'message':"Ajout au panier avec succès","control_process":True})
    return jsonify({'message':'Verifier les information',"control_process":False })


#Ajout au panier
@apis.route('/produit_supprimer/<int:id>',methods=['DELETE'])
@token_required
def produit_suprimer(current_user, id):
    """ Cette fonction retourne une variable control_process: True en cas de réussité du processus
        dans le cas contraire
    """
    if not id:
        return jsonify({'message':"Vérifier les parametres","control_process":False})
    verifcation_porduit_vente=Produit.query.filter_by(id=id).first()
    if verifcation_porduit_vente is None :
        return jsonify({'message':"Ce produit n'existe pas","control_process":False})
    else:
        commande_ajout=Commandes.query.filter_by(user_id=current_user.id, produit_id=id).delete()
        db.session.commit()
        return jsonify({'message':"Suppression avec success","control_process":True})
    return jsonify({'message':'Verifier les information',"control_process":False })

#Diminution de la vente
@apis.route('/produit_panier_moins/<int:id>',methods=['POST','GET','PUT'])
@token_required
def produit_vente_moins(current_user, id):
    """ Cette fonction retourne une variable control_process: True en cas de réussité du processus
        dans le cas contraire
    """
    data=request.get_json()

    if not id:
        return jsonify({'message':"Vérifier les parametres","control_process":False})

    produi_schema = ProduitSchema()
    produits_schema = ProduitSchema(many=True)

    verifcation_porduit_vente=Produit.query.filter_by(id=id).first()
    if verifcation_porduit_vente is None :
        return jsonify({'message':"Ce produit n'existe pas","control_process":False})
    else:
        commande_ajout=Commandes.query.filter_by(user_id=current_user.id, produit_id=id).first()
        if commande_ajout is None:
            valeur_commande= float(data['qte']) * float(verifcation_porduit_vente.prix_p)
            enregistrement_commande=Commandes(qte=data['qte'], somme=valeur_commande, user_id=current_user.id, produit_id=id)
            db.session.add(enregistrement_commande)
            db.session.commit()
            return jsonify({'message':"Ajout au panier avec succès","control_process":True})
        else:
            valeur_commande_entree= float(data['qte']) * float(verifcation_porduit_vente.prix_p)
            if commande_ajout.qte > data['qte'] :
                qte_nouvelle = commande_ajout.qte - data['qte']
                valeur_commande_noubelle= valeur_commande_entree + float(commande_ajout.somme) 
                commande_ajout.qte=qte_nouvelle
                commande_ajout.somme=valeur_commande_noubelle
                db.session.commit()
                return jsonify({'message':"Diminution au panier avec succès","control_process":True})
            else:
                return jsonify({'message':'La quantité est superieur à la quantité disponible',"control_process":False })
    return jsonify({'message':'Verifier les information',"control_process":False })


#Liste le panier des produits
@apis.route('/panier',methods=['GET'])
@token_required
def panier(current_user):
    """ Cette fonction retourne le panier du client avec la veleur totale de l'utilisateur """
    valeur_produit_panier=[]
    commandes_schema = CommandesSchema(many=True)
    commandes_client=Commandes.query.filter_by(user_id=current_user.id).all()
    if commandes_client==[]:
        return jsonify({'message':'Aucun produit dans le panier',"control_process":False})
    for commande_valeur in commandes_client:
      i=commande_valeur.somme
      valeur_produit_panier.insert(0,i)
    valeur_totale=sum(valeur_produit_panier)
    panier_produit=commandes_schema.dump(commandes_client) 
    
    return jsonify({'panier':panier_produit, 'valeur':valeur_totale,"control_process":True })



#Liste commandé produit
@apis.route('/commander',methods=['POST','GET','DELETE','PUT'])
@token_required
def commander(current_user):
    """ Cette fonction retourne la variable control_process en True, si la commande a reussi et False si vous n'avez rien dans le panier """
    valeur_produit_panier=[]
    commandes_schema = CommandesSchema(many=True)
    commandes_client=Commandes.query.filter_by(user_id=current_user.id).all()
    if commandes_client==[]:
        return jsonify({'message':'Aucun produit dans le panier',"control_process":False})

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

    return jsonify({'message':"Commande reussie", "control_process":True })


#Liste commandé produit
@apis.route('/commandes/<int:id>',methods=['GET'])
@token_required
def commande_utilisateur(current_user, id):
    """ Cette fonction retourne liste des produit du panier, la valeur totale du panier et control_process True dans le cas 
    contraire control_procesd est False """

    enre_facture_montant=Facture.query.filter_by(id=id).first()

    if enre_facture_montant is None:
        return jsonify({'message':"Cette commande n'existe pas","control_process":False})

    panier_des_donnes=Panier.query.filter_by(facture_id=id).all()
    if panier_des_donnes==[]:
        return jsonify({'message':"Aucun produit dans la commande","control_process":False})
    paniers_schema=PanierSchema(many=True)
    commande_pan=paniers_schema.dump(panier_des_donnes)

    #Valeur total de la commande
    val_com_facture=[]
    for  paniers in panier_des_donnes:
        i=paniers.valeur
        val_com_facture.insert(0,i)
    valeur_totale_panier=sum(val_com_facture)

    return jsonify({'message':'Produit de commande', 'commande':commande_pan,"valeur_panier":valeur_totale_panier,"control_process":True })


#Liste des produits en exposition
@apis.route('/commandes',methods=['GET'])
@token_required
def commandes(current_user):
    """ Cette fonction retourne la liste des commandes"""
    commande=Facture.query.filter_by(user_id=current_user.id).all()
    if commande == []:
        return jsonify({'message':"Aucune commande disponible","control_process":False})
    commandes_schema = FactureSchema(many=True)
    toutes_commandes=commandes_schema.dump(commande) 
    return jsonify({'commandes':toutes_commandes,'message':"Liste des commandes","control_process":True})


#Liste des categories
@apis.route('/categories',methods=['GET'])
@token_required
def categorie(current_user):
    """ Cette fonction retourne la liste des commandes"""
    categories=Categorie.query.filter_by(statut=True).all()
    if categories == []:
        return jsonify({'message':"Aucune categorie n'est disponible","control_process":False})
    categorie_schema = CategorieSchema(many=True)
    toutes_categorie=categorie_schema.dump(categories) 
    return jsonify({'categorie':toutes_categorie,'message':"Listes des categories","control_process":True})

#Liste des produits en exposition
@apis.route('/categories/<int:id>',methods=['GET'])
@token_required
def categorie_produit(current_user, id):
    """ Cette fonction retourne la liste des commandes"""
    categories=Categorie.query.filter_by(id=id).first()
    if categories is None:
        return jsonify({'message':"Aucune categorie n'est disponible","control_process":False})

    produit_categorie=Produit.query.filter_by(statut=True, categorie_id=id).all()
    produits_schema = ProduitSchema(many=True)
    produits_categorie=produits_schema.dump(produit_categorie) 
    return jsonify({'produits':produits_categorie,'message':"Liste des produit par catégorie","control_process":True})


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


