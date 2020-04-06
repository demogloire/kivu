from app import db, login_manager
from datetime import datetime, date
from flask_login import UserMixin, current_user
from sqlalchemy.orm import backref

@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))

class Types(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    nom = db.Column(db.String(128))
    categories = db.relationship('Categorie', backref='type_categorie', lazy='dynamic')
    def __repr__(self):
        return ' {} '.format(self.nom)

class Trucking(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    tracking_number = db.Column(db.String(255))
    ville_provenance = db.Column(db.String(125))
    provenance = db.Column(db.String(125))
    destination = db.Column(db.String(125))
    date_envoi=db.Column(db.DateTime, nullable=False, default=datetime.utcnow )
    date_livraison=db.Column(db.DateTime )
    encours = db.Column(db.Boolean, default=False)
    statut = db.Column(db.Boolean, default=False)
    transits = db.relationship('Transit', backref='trucking_transit', lazy='dynamic')
    def __repr__(self):
        return ' {} '.format(self.tracking_number)

class Transit(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    en_transit = db.Column(db.String(255))
    ville_transit = db.Column(db.String(125))
    date_envoi_transit=db.Column(db.DateTime, nullable=False, default=datetime.utcnow )
    resume = db.Column(db.Text)
    trucking_id = db.Column(db.Integer, db.ForeignKey('trucking.id'), nullable=False)
    def __repr__(self):
        return ' {} '.format(self.en_transit)

class Categorie(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    nom = db.Column(db.String(128))
    statut = db.Column(db.Boolean, default=False)  
    type_id = db.Column(db.Integer, db.ForeignKey('types.id'), nullable=False)
    produits = db.relationship('Produit', backref='categorie_produit', lazy='dynamic')
    articles = db.relationship('Article', backref='produit_article', lazy='dynamic')
    def __repr__(self):
        return ' {} '.format(self.nom)

class Produit(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    nom = db.Column(db.String(128))
    prix_p = db.Column(db.DECIMAL(precision=10, scale=2, asdecimal=False))
    code= db.Column(db.String(128))
    img_url= db.Column(db.Text)
    description = db.Column(db.Text)
    mesure = db.Column(db.String(128))
    categorie_id = db.Column(db.Integer, db.ForeignKey('categorie.id'), nullable=False)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    commandes = db.relationship('Commandes', backref='produit_commande', lazy='dynamic')
    statut = db.Column(db.Boolean, default=False) 
    def __repr__(self):
        return ' {} '.format(self.nom)


class Article(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    titre = db.Column(db.String(128))
    resume = db.Column(db.Text)
    active= db.Column(db.String(128))
    categorie_id = db.Column(db.Integer, db.ForeignKey('categorie.id'), nullable=False)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    statut = db.Column(db.Boolean, default=False) 
    image_art=db.Column(db.String(200))
    date_pub=db.Column(db.DateTime, nullable=False, default=datetime.utcnow )
    def __repr__(self):
        return ' {} '.format(self.nom)


class Commandes(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    qte = db.Column(db.DECIMAL(precision=10, scale=2, asdecimal=False))
    somme = db.Column(db.DECIMAL(precision=10, scale=2, asdecimal=False))
    nom_client=db.Column(db.String(128))
    tel=db.Column(db.String(128))
    mail=db.Column(db.String(128))
    adr=db.Column(db.String(128))
    produit_id = db.Column(db.Integer, db.ForeignKey('produit.id'), nullable=False)
    date_commande=db.Column(db.DateTime, nullable=False, default=datetime.utcnow )
    description_liv=db.Column(db.Text)
    date_commande_liv=db.Column(db.DateTime, nullable=False, default=datetime.utcnow )
    statut_liv=db.Column(db.Boolean, default=False) 
    annul_liv=db.Column(db.Boolean, default=False) 

class User(db.Model, UserMixin):
    id = db.Column(db.Integer, primary_key=True)
    nom = db.Column(db.String(128))
    post_nom = db.Column(db.String(128))
    prenom= db.Column(db.String(128))
    role = db.Column(db.String(128))
    username = db.Column(db.String(128))
    password = db.Column(db.String(128))
    statut=db.Column(db.Boolean, default=False) 
    produits = db.relationship('Produit', backref='user_produit', lazy='dynamic')
    articles = db.relationship('Article', backref='user_article', lazy='dynamic')

    def __repr__(self):
        return ' {} '.format(self.nom)

class Devis(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    nom = db.Column(db.String(128))
    email = db.Column(db.String(128))
    datedevis=db.Column(db.Date, default=date.today())
    def __repr__(self):
        return ' {} '.format(self.nom)

