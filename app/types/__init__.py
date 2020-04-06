from flask import Blueprint

types = Blueprint('types', __name__, url_prefix='/classification')
# never forget 
from . import routes