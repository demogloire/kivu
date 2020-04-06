from flask import Blueprint

auth = Blueprint('auth', __name__, url_prefix='/authentification')
# never forget 
from . import routes