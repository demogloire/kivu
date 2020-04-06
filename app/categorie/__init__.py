from flask import Blueprint

categorie = Blueprint('categorie', __name__, url_prefix='/categorisation')
# never forget 
from . import routes