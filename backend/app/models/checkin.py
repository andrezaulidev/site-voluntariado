from app import db
from datetime import datetime

class CheckIn(db.Model):
    """Modelo para check-in de voluntários (QR code)"""
    
    __tablename__ = 'checkins'
    
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    qrcode_session_id = db.Column(db.Integer, db.ForeignKey('qrcode_sessions.id'))
    
    # Check-in
    check_in_time = db.Column(db.DateTime, default=datetime.utcnow)
    check_out_time = db.Column(db.DateTime)
    latitude = db.Column(db.Float)
    longitude = db.Column(db.Float)
    
    # Horas
    hours_worked = db.Column(db.Float, default=0)
    
    # Notas
    notes = db.Column(db.Text)
    
    # Relacionamentos
    qrcode_session = db.relationship('QRCodeSession', backref='checkins')
    
    def to_dict(self):
        """Converte para dicionário"""
        return {
            'id': self.id,
            'user_id': self.user_id,
            'user_name': self.user.name if self.user else None,
            'qrcode_session_id': self.qrcode_session_id,
            'check_in_time': self.check_in_time.isoformat(),
            'check_out_time': self.check_out_time.isoformat() if self.check_out_time else None,
            'latitude': self.latitude,
            'longitude': self.longitude,
            'hours_worked': self.hours_worked,
            'notes': self.notes
        }
    
    def __repr__(self):
        return f'<CheckIn {self.user.name} at {self.check_in_time}>'
