import os
import secrets

class Config:
    SQLALCHEMY_DATABASE_URI = os.environ.get('DATABASE_URL')
    SECRET_KEY = os.environ.get('SECRET_KEY')
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    BREVO_API_KEY = os.environ.get('BREVO_API_KEY')
    JWT_SECRET_KEY = os.environ.get('SECRET_KEY')

