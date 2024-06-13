import os

class Config:
    SQLALCHEMY_DATABASE_URI = 'sqlite:///social_media_app.db'
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    JWT_SECRET_KEY = 'your_jwt_secret_key'
