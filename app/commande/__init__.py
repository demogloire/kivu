from flask import Blueprint

commande = Blueprint('commande', __name__, url_prefix='/commande')
# never forget 
from . import routes