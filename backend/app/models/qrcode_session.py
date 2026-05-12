from app import db
from datetime import datetime
import secrets

class QRCodeSession(db.Model):
    """Modelo para sessões de QR code (eventos)"""
    
    __tablename__ = 'qrcode_sessions'
    
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(120), nullable=False)
    description = db.Column(db.Text)
    
    # Datas e horários
    scheduled_date = db.Column(db.DateTime, nullable=False)
    start_time = db.Column(db.DateTime, nullable=False)
    end_time = db.Column(db.DateTime)
    
    # Localização
    latitude = db.Column(db.Float)
    longitude = db.Column(db.Float)
    address = db.Column(db.String(255))
    
    # QR Code
    qrcode_token = db.Column(db.String(128), unique=True, default=lambda: secrets.token_urlsafe(32))
    qrcode_image_path = db.Column(db.String(255))
    
    # Status
    is_active = db.Column(db.Boolean, default=True)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    
    # Relacionamentos
    checkins = db.relationship('CheckIn', backref='session', lazy=True, cascade='all, delete-orphan')
    
    def to_dict(self):
        """Converte para dicionário"""
        return {
            'id': self.id,
            'name': self.name,
            'description': self.description,
            'scheduled_date': self.scheduled_date.isoformat(),
            'start_time': self.start_time.isoformat(),
            'end_time': self.end_time.isoformat() if self.end_time else None,
            'latitude': self.latitude,
            'longitude': self.longitude,
            'address': self.address,
            'qrcode_token': self.qrcode_token,
            'qrcode_image_path': self.qrcode_image_path,
            'is_active': self.is_active,
            'checkins_count': len(self.checkins),
            'created_at': self.created_at.isoformat()
        }
    
    def __repr__(self):
        return f'<QRCodeSession {self.name}>'
