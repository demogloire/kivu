import os
import json
from decimal import Decimal
from flask import jsonify, request, make_response
from .. import db, bcrypt
from ..models import User, Commandes, CommandesSchema, Facture 
import jwt
import datetime
from functools import wraps
from app import create_app

config_name = os.getenv('FLASK_CONFIG')
app = create_app(config_name)


class DecimalEncoder(json.JSONEncoder):
    def default(self, o):
        if isinstance(o, Decimal):
            return float(o)
        return super(DecimalEncoder, self).default(o)

def token_required(f):
    @wraps(f)
    def decorated(*args, **kwargs):
        
        token = None

        if 'x-access-token' in request.headers:
            token = request.headers['x-access-token']
           
        if not token:
            return jsonify({'message': 'Validé la clé de sécurité'}), 401
        try:
            data = jwt.decode(token, app.config['SECRET_KEY'])
            current_user = User.query.filter_by(public_id=data['public_id']).first()
        except:
            return jsonify({'message': "La clé est incorrect"}), 401
        return f(current_user, *args, **kwargs)
    return decorated

@token_required
def codecommande(current_user):
    commande_api=Facture.query.filter_by(user_id=current_user.id).order_by(Facture.id.desc()).first()
    commande_encours=None
    if commande_api is None:
        commande_encours=1
    else:
        commande_encours=commande_api.id+1
    codecommande_encours_unique="#{}{}".format(commande_encours, current_user.id) # Code de la commande

    return codecommande_encours_unique

@token_required
def produit_du_panier(current_user):
    # Les produits du panier
    panier=[]
    commandes_client=Commandes.query.filter_by(user_id=current_user.id).all()
    for produit in commandes_client:
        i=produit.id
        panier.insert(0,i)
    return len(panier)


def produit_simulaire(id):
    verifcation_porduit_vente=Produit.query.filter_by(id=id).first()
    les_memes_categories=[]
    produit_meme_cat=Produit.query.filter_by(categorie_id=verifcation_porduit_vente.categorie_id).all()

    for produit in produit_meme_cat:
        p={
            'id': produit.id,
            'nom': produit.nom,
            'prix_p':produit.prix_p,
            'code':produit.code,
            'img_url':produit.img_url,
            'description_android':produit.description_android,
            'mesure': produit.mesure,
        }
        les_memes_categories.insert(0,p)
    return les_memes_categories
