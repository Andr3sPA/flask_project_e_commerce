from __future__ import print_function
import sib_api_v3_sdk
from flask import Flask
from flask_bcrypt import Bcrypt
from flask_login import LoginManager
from flask_sqlalchemy import SQLAlchemy
from flask_cors import CORS
from config import Config

configuration = None  # Definir como variable global
db = SQLAlchemy()
login_manager = LoginManager()
bcrypt = Bcrypt()
def create_app():
    app = Flask(__name__)
    app.config.from_object(Config)

    # Inicializar extensiones
    db.init_app(app)
    login_manager.init_app(app)
    bcrypt.init_app(app)
    CORS(app)
    global configuration
    configuration = sib_api_v3_sdk.Configuration()
    configuration.api_key['api-key'] = app.config['BREVO_API_KEY']

    return app
