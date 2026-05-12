from flask import Blueprint, request, jsonify
from flask_jwt_extended import create_access_token, jwt_required, get_jwt_identity
from app import db, mail
from app.models.user import User
from flask_mail import Message
from datetime import datetime

bp = Blueprint('auth', __name__, url_prefix='/api/auth')

@bp.route('/register', methods=['POST'])
def register():
    """Registra um novo usuário"""
    try:
        data = request.get_json()
        
        if not data or not all(k in data for k in ['name', 'email', 'password']):
            return jsonify({'message': 'Dados incompletos'}), 400
        
        if User.query.filter_by(email=data['email']).first():
            return jsonify({'message': 'Email já registrado'}), 400
        
        user = User(
            name=data['name'],
            email=data['email'],
            role=data.get('role', 'volunteer'),
            is_active=True
        )
        user.set_password(data['password'])
        
        db.session.add(user)
        db.session.commit()
        
        # Enviar email de boas-vindas (opcional)
        send_welcome_email(user)
        
        return jsonify({
            'message': 'Usuário registrado com sucesso',
            'user': user.to_dict()
        }), 201
    
    except Exception as e:
        db.session.rollback()
        return jsonify({'message': f'Erro: {str(e)}'}), 500

@bp.route('/login', methods=['POST'])
def login():
    """Faz login e retorna JWT token"""
    try:
        data = request.get_json()
        
        if not data or not all(k in data for k in ['email', 'password']):
            return jsonify({'message': 'Email e senha obrigatórios'}), 400
        
        user = User.query.filter_by(email=data['email']).first()
        
        if not user or not user.check_password(data['password']):
            return jsonify({'message': 'Email ou senha incorretos'}), 401
        
        if not user.is_active:
            return jsonify({'message': 'Usuário inativo'}), 403
        
        # Atualizar last_login
        user.last_login = datetime.utcnow()
        db.session.commit()
        
        # Gerar token JWT
        access_token = create_access_token(identity=user.id)
        
        return jsonify({
            'message': 'Login realizado com sucesso',
            'access_token': access_token,
            'user': user.to_dict()
        }), 200
    
    except Exception as e:
        return jsonify({'message': f'Erro: {str(e)}'}), 500

@bp.route('/me', methods=['GET'])
@jwt_required()
def get_current_user():
    """Retorna dados do usuário atual"""
    try:
        user_id = get_jwt_identity()
        user = User.query.get(user_id)
        
        if not user:
            return jsonify({'message': 'Usuário não encontrado'}), 404
        
        return jsonify({
            'user': user.to_dict(),
            'volunteer': user.volunteer.to_dict() if user.volunteer else None
        }), 200
    
    except Exception as e:
        return jsonify({'message': f'Erro: {str(e)}'}), 500

@bp.route('/change-password', methods=['POST'])
@jwt_required()
def change_password():
    """Muda a senha do usuário"""
    try:
        user_id = get_jwt_identity()
        user = User.query.get(user_id)
        data = request.get_json()
        
        if not user:
            return jsonify({'message': 'Usuário não encontrado'}), 404
        
        if not user.check_password(data.get('current_password')):
            return jsonify({'message': 'Senha atual incorreta'}), 401
        
        if not data.get('new_password'):
            return jsonify({'message': 'Nova senha obrigatória'}), 400
        
        user.set_password(data['new_password'])
        db.session.commit()
        
        return jsonify({'message': 'Senha alterada com sucesso'}), 200
    
    except Exception as e:
        db.session.rollback()
        return jsonify({'message': f'Erro: {str(e)}'}), 500

def send_welcome_email(user):
    """Envia email de boas-vindas"""
    try:
        msg = Message(
            subject='Bem-vindo ao Marmita Solidária!',
            recipients=[user.email],
            html=f"""
            <h2>Bem-vindo, {user.name}!</h2>
            <p>Obrigado por se registrar no Marmita Solidária!</p>
            <p>Sua inscrição foi confirmada e você já está pronto para começar.</p>
            <p>Em breve, você receberá más informações sobre o evento.</p>
            <hr>
            <p>Marmita Solidária 2026 💛</p>
            """
        )
        mail.send(msg)
    except Exception as e:
        print(f"Erro ao enviar email: {e}")
