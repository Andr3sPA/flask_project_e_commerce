from flask import Flask
from flask_bcrypt import Bcrypt
from flask_jwt_extended import JWTManager
from flask_sqlalchemy import SQLAlchemy
from flask_cors import CORS
from config import Config
from datetime import timedelta
import sib_api_v3_sdk
from sib_api_v3_sdk import Configuration

# Inicialización de extensiones
db = SQLAlchemy()
bcrypt = Bcrypt()


def create_app():
    app = Flask(__name__)
    app.config.from_object(Config)

    # Inicializar extensiones
    db.init_app(app)
    bcrypt.init_app(app)

    # Configuración de JWT
    app.config["JWT_COOKIE_SECURE"] = True
    app.config["JWT_TOKEN_LOCATION"] = ["cookies"]
    app.config["JWT_ACCESS_TOKEN_EXPIRES"] = timedelta(hours=1)
    app.config["JWT_REFRESH_TOKEN_EXPIRES"] = timedelta(days=30)

    jwt = JWTManager(app)
    CORS(app, supports_credentials=True)

    # Configuración de Brevo
    configuration = Configuration()
    configuration.api_key['api-key'] = app.config['BREVO_API_KEY']

    return app

