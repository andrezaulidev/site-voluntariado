from app import db
from datetime import datetime
import json

class Volunteer(db.Model):
    """Modelo para dados de voluntários"""
    
    __tablename__ = 'volunteers'
    
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False, unique=True)
    
    # Dados pessoais
    age = db.Column(db.Integer)
    phone = db.Column(db.String(20))
    class_year = db.Column(db.String(50))  # Turma/série
    
    # Contribuição
    contributions = db.Column(db.JSON, default=list)  # ['arrecadar', 'preparar', ...]
    observations = db.Column(db.Text)
    
    # Geolocalização
    latitude = db.Column(db.Float)
    longitude = db.Column(db.Float)
    address = db.Column(db.String(255))
    
    # Status
    status = db.Column(db.String(20), default='enrolled')  # enrolled, confirmed, attended, cancelled
    hours_contributed = db.Column(db.Float, default=0)
    
    # Timestamps
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    
    # Relacionamentos
    checkins = db.relationship('CheckIn', backref='volunteer', lazy=True, cascade='all, delete-orphan')
    
    def get_contributions_list(self):
        """Retorna lista de contribuições"""
        if isinstance(self.contributions, str):
            return json.loads(self.contributions)
        return self.contributions or []
    
    def to_dict(self):
        """Converte para dicionário"""
        return {
            'id': self.id,
            'user_id': self.user_id,
            'name': self.user.name,
            'email': self.user.email,
            'age': self.age,
            'phone': self.phone,
            'class_year': self.class_year,
            'contributions': self.get_contributions_list(),
            'observations': self.observations,
            'latitude': self.latitude,
            'longitude': self.longitude,
            'address': self.address,
            'status': self.status,
            'hours_contributed': self.hours_contributed,
            'created_at': self.created_at.isoformat(),
            'updated_at': self.updated_at.isoformat()
        }
    
    def __repr__(self):
        return f'<Volunteer {self.user.name}>'
