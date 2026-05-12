from flask import Blueprint

bp = Blueprint('routes', __name__)

# Importar blueprints
from . import auth_bp, volunteers_bp, admin_bp, qrcode_bp
