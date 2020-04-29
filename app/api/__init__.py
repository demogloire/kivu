from flask import Blueprint

apis = Blueprint('apis', __name__, url_prefix='/api')
# never forget 
from . import routes