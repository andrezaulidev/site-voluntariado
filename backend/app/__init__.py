from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_jwt_extended import JWTManager
from flask_cors import CORS
from flask_mail import Mail
import os

db = SQLAlchemy()
jwt = JWTManager()
mail = Mail()

def create_app(config_name=None):
    """Factory para criar a aplicação Flask"""
    
    if config_name is None:
        config_name = os.getenv('FLASK_ENV', 'development')
    
    from config import config
    
    app = Flask(__name__)
    app.config.from_object(config[config_name])
    
    # Inicializar extensões
    db.init_app(app)
    jwt.init_app(app)
    mail.init_app(app)
    CORS(app, resources={r"/api/*": {"origins": "*"}})
    
    # Registrar blueprints
    from app.routes import auth_bp, volunteers_bp, admin_bp, qrcode_bp
    
    app.register_blueprint(auth_bp.bp)
    app.register_blueprint(volunteers_bp.bp)
    app.register_blueprint(admin_bp.bp)
    app.register_blueprint(qrcode_bp.bp)
    
    # Criar tabelas
    with app.app_context():
        db.create_all()
        
        # Criar admin padrão
        from app.models.user import User
        admin = User.query.filter_by(email='admin@marmitasolidaria.com').first()
        if not admin:
            admin = User(
                name='Administrator',
                email='admin@marmitasolidaria.com',
                password='admin123',
                role='admin',
                is_active=True
            )
            db.session.add(admin)
            db.session.commit()
            print("✓ Admin padrão criado: admin@marmitasolidaria.com / admin123")
    
    return app
