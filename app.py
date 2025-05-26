import os

from flask import Flask, redirect, render_template, session, url_for
from flask_login import LoginManager

from models import Users

app = Flask(__name__)
app.secret_key = os.getenv("SECRET_KEY", "is_a_very_secret_key")


login_manager = LoginManager()
login_manager.login_view = "login"
login_manager.login_message = "NEED LOGIN"
login_manager.init_app(app)

@login_manager.user_loader
def load_user(user_id):
    user = Users.get(user_id)
    print(user)
    return user

from routes.main import *
from routes.users import *
from routes.messager import *
    
    
if __name__ == "__main__":
    print(app.url_map)
    app.run(debug=True, port=5050)
