from app import db
from datetime import datetime
from werkzeug.security import generate_password_hash, check_password_hash

class User(db.Model):
    """Modelo para usuários (admin e voluntários)"""
    
    __tablename__ = 'users'
    
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(120), nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False, index=True)
    password_hash = db.Column(db.String(255), nullable=False)
    role = db.Column(db.String(20), default='volunteer')  # admin, volunteer, coordinator
    is_active = db.Column(db.Boolean, default=True)
    email_verified = db.Column(db.Boolean, default=False)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    last_login = db.Column(db.DateTime)
    
    # Relacionamentos
    volunteer = db.relationship('Volunteer', backref='user', uselist=False, cascade='all, delete-orphan')
    checkins = db.relationship('CheckIn', backref='user', lazy=True, cascade='all, delete-orphan')
    
    def set_password(self, password):
        """Hash da senha"""
        self.password_hash = generate_password_hash(password)
    
    def check_password(self, password):
        """Verifica a senha"""
        return check_password_hash(self.password_hash, password)
    
    def to_dict(self):
        """Converte para dicionário"""
        return {
            'id': self.id,
            'name': self.name,
            'email': self.email,
            'role': self.role,
            'is_active': self.is_active,
            'email_verified': self.email_verified,
            'created_at': self.created_at.isoformat(),
            'last_login': self.last_login.isoformat() if self.last_login else None
        }
    
    def __repr__(self):
        return f'<User {self.email}>'
