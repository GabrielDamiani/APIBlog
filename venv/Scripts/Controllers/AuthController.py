from flask import request, jsonify, Blueprint, current_app
import datetime
import jwt
from functools import wraps

from ..DatabaseConnection import db
from ..Models.Users import User

login_bp = Blueprint("login_bp", __name__)

@login_bp.route("/login", methods=["POST"])
def login():
    data = request.get_json()
    login = data.get('login')
    password = data.get('password')

    user = User.query.filter_by(Login=login, Active=1).first()

    if user and user.Password == password:
        token = jwt.encode({'user_id': user.Id, 'exp': datetime.datetime.utcnow() + datetime.timedelta(hours=1)}, current_app.config['SECRET_KEY'], algorithm='HS256')
        return jsonify({'token': token}), 200
    else:
        return jsonify({"Mensagem": "Credenciais invalidas, tente novamente"}), 401

def token_required(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        token = None
        if 'Authorization' in request.headers:
            token = request.headers['Authorization'].split(" ")[1]

        if not token:
            return jsonify({'Mensagem': 'Token faltando!'}), 401

        try:
            data = jwt.decode(token, current_app.config['SECRET_KEY'], algorithms=['HS256'])
            current_user = User.query.get(data['user_id'])
        except:
            return jsonify({'Mensagem': 'Token invalido!'}), 401

        return f(current_user, *args, **kwargs)
    return decorated_function
