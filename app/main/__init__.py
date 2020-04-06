from flask import Blueprint

main = Blueprint('main', __name__, url_prefix='/dashboard')
# never forget 
from . import routes