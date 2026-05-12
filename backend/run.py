#!/usr/bin/env python
"""
Aplicação Principal - Marmita Solidária Backend
"""

import os
import sys
from app import create_app, db

app = create_app(os.getenv('FLASK_ENV', 'development'))

@app.shell_context_processor
def make_shell_context():
    """Contexto para Flask shell"""
    return {
        'db': db,
    }

@app.cli.command()
def init_db():
    """Inicializa o banco de dados"""
    db.create_all()
    print("✓ Banco de dados inicializado!")

@app.cli.command()
def drop_db():
    """Deleta o banco de dados (CUIDADO!)"""
    if input("Tem certeza? (s/n): ").lower() == 's':
        db.drop_all()
        print("✓ Banco de dados deletado!")

@app.cli.command()
def seed_db():
    """Popula o banco com dados de teste"""
    from app.models.user import User
    from app.models.qrcode_session import QRCodeSession
    from datetime import datetime, timedelta
    
    # Criar admin
    admin = User(
        name='Admin',
        email='admin@marmita.local',
        role='admin',
        is_active=True
    )
    admin.set_password('admin123')
    db.session.add(admin)
    
    # Criar sessão de teste
    session = QRCodeSession(
        name='Marmita Solidária 2026',
        description='Evento principal de distribuição de marmitas',
        scheduled_date=datetime.utcnow() + timedelta(days=7),
        start_time=datetime.utcnow() + timedelta(days=7, hours=9),
        end_time=datetime.utcnow() + timedelta(days=7, hours=13),
        latitude=-23.5505,  # São Paulo
        longitude=-46.6333,
        address='Escola Paulo de Tarso, São Paulo'
    )
    db.session.add(session)
    db.session.commit()
    
    print("✓ Banco de dados populado com dados de teste!")

if __name__ == '__main__':
    app.run(debug=True, host='127.0.0.1', port=5000)
