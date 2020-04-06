from flask import Blueprint

plate = Blueprint('plate', __name__, url_prefix='/')
# never forget 
from . import routes