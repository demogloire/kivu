import os
from flask import Flask, render_template
from flask_bcrypt import Bcrypt
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager
from flask_migrate import Migrate
#from wtf_tinymce import wtf_tinymce
from flask_simplemde import SimpleMDE
from flaskext.markdown import Markdown
from flask_marshmallow import Marshmallow
#from flask_minify import minify
#Importation des configuration de l'application sur le developpement de l'application
from config import app_config



db = SQLAlchemy()
login_manager = LoginManager()
bcrypt = Bcrypt()
ma = Marshmallow()
#Structure de l'application

def create_app(config_name):
    app = Flask(__name__, instance_relative_config=True)
    app.config.from_object(app_config[config_name])
    app.config.from_pyfile('config.py')

    app.config.from_mapping(
        CLOUDINARY_URL=os.environ.get('CLOUDINARY_URL') or 'Pegue a sua Key',
    )


    #Bootstrap(app)
    db.init_app(app)
    bcrypt.init_app(app)
    login_manager.init_app(app)
    Markdown(app)
    migrate = Migrate(app, db)
    
    #minify(app=app, html=True, js=True, cssless=True)
    #wtf_tinymce.init_app(app)
    

    login_manager.login_message = "Veuillez vous connecté"
    login_manager.login_view = "auth.login"
    login_manager.login_message_category ='danger'
    #SimpleMDE(app)

    #md= Markdown(app, extensions=['fenced_code'])
    from app import models


    @app.errorhandler(403)
    def forbidden(error):
        rec={'titre':'Erreur 403', 'page':'Forbidden'}
        return render_template('errors/403.html', title='Forbidden', rec=rec), 403

    @app.errorhandler(404)
    def page_not_found(error):
        rec={'titre':'Erreur 404', 'page':'Page non trouvée'}
        return render_template('errors/404.html', title='Page non trouvée', rec=rec), 404

    @app.errorhandler(500)
    def internal_server_error(error):
        rec={'titre':'Erreur 505', 'page':'Erreur serveur'}
        return render_template('errors/500.html', title='Erreur serveur'), 500


    #Login
    from .authentification import auth as auth_blueprint
    app.register_blueprint(auth_blueprint)

    #Utilisateur
    from .user import user as user_blueprint
    app.register_blueprint(user_blueprint)

    #Main
    from .main import main as main_blueprint
    app.register_blueprint(main_blueprint)

    #Types des categorie
    from .types import types as types_blueprint
    app.register_blueprint(types_blueprint)

    #Categorie
    from .categorie import categorie as categorie_blueprint
    app.register_blueprint(categorie_blueprint)

    #Produit
    from .produit import produit as produit_blueprint
    app.register_blueprint(produit_blueprint)
 
    #Les internautes
    from .plateforme import plate as plate_blueprint
    app.register_blueprint(plate_blueprint)

    #Les trucking
    from .trucking import trucking as trucking_blueprint
    app.register_blueprint(trucking_blueprint)

    #Les commandes
    from .commande import commande as commande_blueprint
    app.register_blueprint(commande_blueprint)

    #Les commandes
    from .api import apis as api_blueprint
    app.register_blueprint(api_blueprint)

    return app

from . import models