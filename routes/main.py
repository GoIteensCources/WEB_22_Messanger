from flask import flash, redirect, render_template, request, session, url_for
from flask_login import login_required, login_user, logout_user

from app import app

from flask_login import current_user


@app.route("/")
@app.route("/home")
@login_required
def index():    
    return render_template("index.html", username = current_user.username)
