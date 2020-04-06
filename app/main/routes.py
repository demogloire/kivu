from flask import render_template, flash, url_for, redirect, request, session
from .. import db, bcrypt
from ..models import User 
#from app.user.forms import AjouteruserForm, PassuserForm, EditeruserForm
from flask_login import login_user, current_user, logout_user, login_required
from . import main

@main.route('/administration', methods=['GET', 'POST'])
@login_required
def dashboard():
   title='Dashboard | Kivu Exchange'
   return render_template('main/main.html',  title=title)

@main.route('/configuration', methods=['GET', 'POST'])
@login_required
def config():
   title='Dashboard | Kivu Exchange'
   return render_template('main/conf.html',  title=title)

@main.route('/conf_produit', methods=['GET', 'POST'])
@login_required
def configpro():
   title='Dashboard | Kivu Exchange'
   return render_template('main/confpro.html',  title=title)