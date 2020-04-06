import os
import secrets
import random
import string
import time
import uuid
from datetime import datetime
from flask import redirect, session, url_for
from dateutil.relativedelta import relativedelta, MO
from functools import wraps
from PIL import Image
from .. import create_app


config_name = os.getenv('FLASK_CONFIG')
app = create_app(config_name)

#Code unique trucking
def trucking_number(length=12):
    #put your letters in the following string
    your_letters='1234567890'
    return ''.join((random.choice(your_letters) for i in range(length)))


def truckin_id(f):
    @wraps(f)
    def wrap(*args, **kwargs):
      if 'truck' in session:
        return f(*args, **kwargs)
      else:
        return redirect(url_for('trucking.littruck'))
    return wrap

def save_picture(form_picture):
    random_hex = secrets.token_hex(8)
    _, f_ext = os.path.splitext(form_picture.filename)
    picture_fn = random_hex + f_ext
    picture_path = os.path.join(app.root_path, 'static/produit', picture_fn)
    output_sz = (370,350)
    i= Image.open(form_picture)
    i.thumbnail(output_sz)
    i.save(picture_path)
    return picture_fn