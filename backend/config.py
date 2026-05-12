import os
from datetime import timedelta
from dotenv import load_dotenv

load_dotenv()

class Config:
    """Configurações base"""
    SECRET_KEY = os.getenv('SECRET_KEY', 'chave-desenvolvimento')
    SQLALCHEMY_DATABASE_URI = os.getenv('DATABASE_URL', 'sqlite:///marmita.db')
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    
    # JWT
    JWT_SECRET_KEY = os.getenv('JWT_SECRET_KEY', 'jwt-chave-desenvolvimento')
    JWT_ACCESS_TOKEN_EXPIRES = timedelta(days=1)
    
    # Email
    MAIL_SERVER = os.getenv('MAIL_SERVER', 'smtp.gmail.com')
    MAIL_PORT = int(os.getenv('MAIL_PORT', 587))
    MAIL_USE_TLS = os.getenv('MAIL_USE_TLS', True)
    MAIL_USERNAME = os.getenv('MAIL_USERNAME', '')
    MAIL_PASSWORD = os.getenv('MAIL_PASSWORD', '')
    MAIL_DEFAULT_SENDER = os.getenv('MAIL_DEFAULT_SENDER', 'noreply@marmitasolidaria.com')
    
    # Frontend
    FRONTEND_URL = os.getenv('FRONTEND_URL', 'http://localhost:8000')

class DevelopmentConfig(Config):
    """Configurações de desenvolvimento"""
    DEBUG = True
    TESTING = False

class ProductionConfig(Config):
    """Configurações de produção"""
    DEBUG = False
    TESTING = False

class TestingConfig(Config):
    """Configurações de testes"""
    TESTING = True
    SQLALCHEMY_DATABASE_URI = 'sqlite:///:memory:'

# Usar config baseado no FLASK_ENV
config = {
    'development': DevelopmentConfig,
    'production': ProductionConfig,
    'testing': TestingConfig,
    'default': DevelopmentConfig
}
