from flask import Blueprint

trucking = Blueprint('trucking', __name__, url_prefix='/trucking')
# never forget 
from . import routes