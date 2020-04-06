from flask import Blueprint

produit = Blueprint('produit', __name__, url_prefix='/produit')
# never forget 
from . import routes