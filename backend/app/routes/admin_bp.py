from flask import Blueprint, request, jsonify
from flask_jwt_extended import jwt_required, get_jwt_identity
from app import db
from app.models.user import User
from app.models.volunteer import Volunteer
from app.models.qrcode_session import QRCodeSession
from functools import wraps

bp = Blueprint('admin', __name__, url_prefix='/api/admin')

def admin_required(fn):
    """Decorator para verificar se é admin"""
    @wraps(fn)
    @jwt_required()
    def wrapper(*args, **kwargs):
        user_id = get_jwt_identity()
        user = User.query.get(user_id)
        
        if not user or user.role != 'admin':
            return jsonify({'message': 'Acesso negado. Apenas admins.'}), 403
        
        return fn(*args, **kwargs)
    return wrapper

@bp.route('/dashboard', methods=['GET'])
@admin_required
def get_dashboard():
    """Dashboard com estatísticas gerais"""
    try:
        total_users = User.query.count()
        total_volunteers = Volunteer.query.count()
        total_sessions = QRCodeSession.query.count()
        
        recent_volunteers = Volunteer.query.order_by(
            Volunteer.created_at.desc()
        ).limit(10).all()
        
        return jsonify({
            'stats': {
                'total_users': total_users,
                'total_volunteers': total_volunteers,
                'total_sessions': total_sessions
            },
            'recent_volunteers': [v.to_dict() for v in recent_volunteers]
        }), 200
    
    except Exception as e:
        return jsonify({'message': f'Erro: {str(e)}'}), 500

@bp.route('/users', methods=['GET'])
@admin_required
def list_users():
    """Lista todos os usuários"""
    try:
        page = request.args.get('page', 1, type=int)
        per_page = request.args.get('per_page', 20, type=int)
        role = request.args.get('role')
        
        query = User.query
        
        if role:
            query = query.filter_by(role=role)
        
        users = query.order_by(User.created_at.desc()).paginate(
            page=page, per_page=per_page
        )
        
        return jsonify({
            'users': [u.to_dict() for u in users.items],
            'total': users.total,
            'pages': users.pages
        }), 200
    
    except Exception as e:
        return jsonify({'message': f'Erro: {str(e)}'}), 500

@bp.route('/users/<int:user_id>/toggle-active', methods=['POST'])
@admin_required
def toggle_user_active(user_id):
    """Ativa/desativa um usuário"""
    try:
        user = User.query.get(user_id)
        
        if not user:
            return jsonify({'message': 'Usuário não encontrado'}), 404
        
        user.is_active = not user.is_active
        db.session.commit()
        
        return jsonify({
            'message': f'Usuário {"ativado" if user.is_active else "desativado"}',
            'user': user.to_dict()
        }), 200
    
    except Exception as e:
        db.session.rollback()
        return jsonify({'message': f'Erro: {str(e)}'}), 500

@bp.route('/sessions', methods=['GET'])
@admin_required
def list_sessions():
    """Lista todas as sessões de QR code"""
    try:
        sessions = QRCodeSession.query.order_by(
            QRCodeSession.scheduled_date.desc()
        ).all()
        
        return jsonify({
            'sessions': [s.to_dict() for s in sessions]
        }), 200
    
    except Exception as e:
        return jsonify({'message': f'Erro: {str(e)}'}), 500

@bp.route('/sessions', methods=['POST'])
@admin_required
def create_session():
    """Cria uma nova sessão de QR code"""
    try:
        from datetime import datetime
        data = request.get_json()
        
        session = QRCodeSession(
            name=data.get('name'),
            description=data.get('description'),
            scheduled_date=datetime.fromisoformat(data['scheduled_date']),
            start_time=datetime.fromisoformat(data['start_time']),
            end_time=datetime.fromisoformat(data['end_time']) if data.get('end_time') else None,
            latitude=data.get('latitude'),
            longitude=data.get('longitude'),
            address=data.get('address')
        )
        
        db.session.add(session)
        db.session.commit()
        
        return jsonify({
            'message': 'Sessão criada com sucesso',
            'session': session.to_dict()
        }), 201
    
    except Exception as e:
        db.session.rollback()
        return jsonify({'message': f'Erro: {str(e)}'}), 500

@bp.route('/reports/volunteers', methods=['GET'])
@admin_required
def generate_volunteer_report():
    """Gera relatório de voluntários em CSV"""
    try:
        from io import StringIO
        
        volunteers = Volunteer.query.all()
        
        output = StringIO()
        output.write('Nome,Email,Idade,Turma,Status,Horas Contribuídas,Data Inscrição\n')
        
        for v in volunteers:
            output.write(
                f'"{v.user.name}","{v.user.email}",{v.age},"{v.class_year}",{v.status},'
                f'{v.hours_contributed},{v.created_at.isoformat()}\n'
            )
        
        return output.getvalue(), 200, {
            'Content-Disposition': 'attachment; filename="volunteers_report.csv"',
            'Content-Type': 'text/csv'
        }
    
    except Exception as e:
        return jsonify({'message': f'Erro: {str(e)}'}), 500

@bp.route('/reports/checkins', methods=['GET'])
@admin_required
def generate_checkin_report():
    """Gera relatório de check-ins"""
    try:
        from app.models.checkin import CheckIn
        
        checkins = CheckIn.query.all()
        
        output = StringIO()
        output.write('Voluntário,Email,Check-in,Check-out,Horas Trabalhadas,Notas\n')
        
        for c in checkins:
            output.write(
                f'"{c.user.name}","{c.user.email}",{c.check_in_time.isoformat()},'
                f'{c.check_out_time.isoformat() if c.check_out_time else ""},'
                f'{c.hours_worked},"{c.notes or ""}"\n'
            )
        
        return output.getvalue(), 200, {
            'Content-Disposition': 'attachment; filename="checkins_report.csv"',
            'Content-Type': 'text/csv'
        }
    
    except Exception as e:
        return jsonify({'message': f'Erro: {str(e)}'}), 500
