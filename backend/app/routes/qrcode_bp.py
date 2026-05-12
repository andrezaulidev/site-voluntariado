from flask import Blueprint, request, jsonify, send_file
from flask_jwt_extended import jwt_required, get_jwt_identity
from app import db
from app.models.user import User
from app.models.qrcode_session import QRCodeSession
from app.models.checkin import CheckIn
from app.utils.geolocation import calculate_distance
import qrcode
from io import BytesIO
import os

bp = Blueprint('qrcode', __name__, url_prefix='/api/qrcode')

@bp.route('/sessions/<int:session_id>/qrcode', methods=['GET'])
def get_qrcode_image(session_id):
    """Retorna imagem do QR code da sessão"""
    try:
        session = QRCodeSession.query.get(session_id)
        
        if not session:
            return jsonify({'message': 'Sessão não encontrada'}), 404
        
        # Gerar QR code
        qr = qrcode.QRCode(
            version=1,
            error_correction=qrcode.constants.ERROR_CORRECT_L,
            box_size=10,
            border=4,
        )
        qr.add_data(f"session_{session.qrcode_token}")
        qr.make(fit=True)
        
        img = qr.make_image(fill_color="black", back_color="white")
        
        img_io = BytesIO()
        img.save(img_io, 'PNG')
        img_io.seek(0)
        
        return send_file(img_io, mimetype='image/png'), 200
    
    except Exception as e:
        return jsonify({'message': f'Erro: {str(e)}'}), 500

@bp.route('/checkin', methods=['POST'])
@jwt_required()
def scan_qrcode_checkin():
    """Faz check-in via QR code"""
    try:
        user_id = get_jwt_identity()
        data = request.get_json()
        
        user = User.query.get(user_id)
        if not user:
            return jsonify({'message': 'Usuário não encontrado'}), 404
        
        # Validar token do QR code
        session = QRCodeSession.query.filter_by(
            qrcode_token=data.get('qrcode_token')
        ).first()
        
        if not session:
            return jsonify({'message': 'QR code inválido'}), 400
        
        # Verificar distância geográfica (máx 100 metros)
        user_lat = data.get('latitude')
        user_lon = data.get('longitude')
        
        if user_lat and user_lon and session.latitude and session.longitude:
            distance = calculate_distance(
                user_lat, user_lon,
                session.latitude, session.longitude
            )
            
            if distance > 0.1:  # más de 100m
                return jsonify({
                    'message': f'Você está muito longe do local ({distance*1000:.0f}m)',
                    'distance_km': distance
                }), 400
        
        # Verificar se já fez check-in hoje
        from datetime import datetime, timedelta
        today = datetime.utcnow().date()
        
        existing_checkin = CheckIn.query.filter(
            and_(
                CheckIn.user_id == user_id,
                CheckIn.qrcode_session_id == session.id,
                db.func.date(CheckIn.check_in_time) == today
            )
        ).first()
        
        if existing_checkin and not existing_checkin.check_out_time:
            return jsonify({
                'message': 'Você já fez check-in nesta sessão hoje'
            }), 400
        
        # Criar check-in
        checkin = CheckIn(
            user_id=user_id,
            qrcode_session_id=session.id,
            latitude=user_lat,
            longitude=user_lon
        )
        
        db.session.add(checkin)
        db.session.commit()
        
        return jsonify({
            'message': 'Check-in realizado com sucesso!',
            'checkin': checkin.to_dict()
        }), 201
    
    except Exception as e:
        db.session.rollback()
        return jsonify({'message': f'Erro: {str(e)}'}), 500

@bp.route('/checkout', methods=['POST'])
@jwt_required()
def scan_qrcode_checkout():
    """Faz check-out via QR code"""
    try:
        user_id = get_jwt_identity()
        data = request.get_json()
        
        checkin_id = data.get('checkin_id')
        checkin = CheckIn.query.get(checkin_id)
        
        if not checkin or checkin.user_id != user_id:
            return jsonify({'message': 'Check-in não encontrado'}), 404
        
        if checkin.check_out_time:
            return jsonify({'message': 'Você já fez check-out'}), 400
        
        # Calcular horas trabalhadas
        from datetime import datetime
        checkout_time = datetime.utcnow()
        hours_worked = (
            (checkout_time - checkin.check_in_time).total_seconds() / 3600
        )
        
        checkin.check_out_time = checkout_time
        checkin.hours_worked = round(hours_worked, 2)
        checkin.notes = data.get('notes')
        
        # Atualizar horas do voluntário
        volunteer = data['check_in_time'].volunteer
        if volunteer:
            volunteer.hours_contributed += hours_worked
        
        db.session.commit()
        
        return jsonify({
            'message': 'Check-out realizado com sucesso!',
            'hours_worked': checkin.hours_worked,
            'checkin': checkin.to_dict()
        }), 200
    
    except Exception as e:
        db.session.rollback()
        return jsonify({'message': f'Erro: {str(e)}'}), 500

@bp.route('/sessions/<int:session_id>/checkins', methods=['GET'])
@jwt_required()
def get_session_checkins(session_id):
    """Retorna todos os check-ins de uma sessão"""
    try:
        user_id = get_jwt_identity()
        user = User.query.get(user_id)
        
        if not user or user.role != 'admin':
            return jsonify({'message': 'Acesso negado'}), 403
        
        session = QRCodeSession.query.get(session_id)
        if not session:
            return jsonify({'message': 'Sessão não encontrada'}), 404
        
        checkins = CheckIn.query.filter_by(qrcode_session_id=session_id).all()
        
        return jsonify({
            'session': session.to_dict(),
            'checkins': [c.to_dict() for c in checkins],
            'total_checkins': len(checkins)
        }), 200
    
    except Exception as e:
        return jsonify({'message': f'Erro: {str(e)}'}), 500
