from flask import Blueprint, request, jsonify
from flask_jwt_extended import jwt_required, get_jwt_identity
from app import db
from app.models.user import User
from app.models.volunteer import Volunteer
from sqlalchemy import and_

bp = Blueprint('volunteers', __name__, url_prefix='/api/volunteers')

@bp.route('', methods=['POST'])
@jwt_required()
def create_volunteer():
    """Cria/atualiza perfil de voluntário"""
    try:
        user_id = get_jwt_identity()
        data = request.get_json()
        
        user = User.query.get(user_id)
        if not user:
            return jsonify({'message': 'Usuário não encontrado'}), 404
        
        # Verificar ou criar volunteer
        volunteer = Volunteer.query.filter_by(user_id=user_id).first()
        
        if not volunteer:
            volunteer = Volunteer(user_id=user_id)
        
        # Atualizar dados
        volunteer.age = data.get('age')
        volunteer.phone = data.get('phone')
        volunteer.class_year = data.get('class_year')
        volunteer.contributions = data.get('contributions', [])
        volunteer.observations = data.get('observations')
        volunteer.latitude = data.get('latitude')
        volunteer.longitude = data.get('longitude')
        volunteer.address = data.get('address')
        volunteer.status = data.get('status', 'enrolled')
        
        db.session.add(volunteer)
        db.session.commit()
        
        return jsonify({
            'message': 'Perfil de voluntário atualizado',
            'volunteer': volunteer.to_dict()
        }), 201
    
    except Exception as e:
        db.session.rollback()
        return jsonify({'message': f'Erro: {str(e)}'}), 500

@bp.route('/<int:volunteer_id>', methods=['GET'])
def get_volunteer(volunteer_id):
    """Retorna dados do voluntário"""
    try:
        volunteer = Volunteer.query.get(volunteer_id)
        
        if not volunteer:
            return jsonify({'message': 'Voluntário não encontrado'}), 404
        
        return jsonify({
            'volunteer': volunteer.to_dict()
        }), 200
    
    except Exception as e:
        return jsonify({'message': f'Erro: {str(e)}'}), 500

@bp.route('', methods=['GET'])
def list_volunteers():
    """Lista todos os voluntários (com filters opcionais)"""
    try:
        page = request.args.get('page', 1, type=int)
        per_page = request.args.get('per_page', 20, type=int)
        status = request.args.get('status')
        
        query = Volunteer.query
        
        if status:
            query = query.filter_by(status=status)
        
        volunteers = query.paginate(page=page, per_page=per_page)
        
        return jsonify({
            'volunteers': [v.to_dict() for v in volunteers.items],
            'total': volunteers.total,
            'pages': volunteers.pages,
            'current_page': page
        }), 200
    
    except Exception as e:
        return jsonify({'message': f'Erro: {str(e)}'}), 500

@bp.route('/stats/summary', methods=['GET'])
def get_stats():
    """Retorna estatísticas dos voluntários"""
    try:
        total_volunteers = Volunteer.query.count()
        enrolled = Volunteer.query.filter_by(status='enrolled').count()
        confirmed = Volunteer.query.filter_by(status='confirmed').count()
        attended = Volunteer.query.filter_by(status='attended').count()
        cancelled = Volunteer.query.filter_by(status='cancelled').count()
        
        total_hours = db.session.query(db.func.sum(Volunteer.hours_contributed)).scalar() or 0
        
        return jsonify({
            'total_volunteers': total_volunteers,
            'enrolled': enrolled,
            'confirmed': confirmed,
            'attended': attended,
            'cancelled': cancelled,
            'total_hours_contributed': float(total_hours)
        }), 200
    
    except Exception as e:
        return jsonify({'message': f'Erro: {str(e)}'}), 500

@bp.route('/geolocation', methods=['GET'])
def get_volunteers_map():
    """Retorna voluntários com geolocalização para mapa"""
    try:
        volunteers = Volunteer.query.filter(
            and_(
                Volunteer.latitude != None,
                Volunteer.longitude != None
            )
        ).all()
        
        return jsonify({
            'volunteers': [
                {
                    'id': v.id,
                    'name': v.user.name,
                    'latitude': v.latitude,
                    'longitude': v.longitude,
                    'address': v.address,
                    'status': v.status
                }
                for v in volunteers
            ]
        }), 200
    
    except Exception as e:
        return jsonify({'message': f'Erro: {str(e)}'}), 500
