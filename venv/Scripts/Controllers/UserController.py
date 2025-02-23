from flask import Blueprint, request, jsonify
from ..DatabaseConnection import db
from ..Models.Users import User
from ..Models.LogUsers import LogUser
from datetime import datetime

user_bp = Blueprint("user_bp", __name__)

@user_bp.route("/users/create", methods=["POST"])
def create_user():
    data = request.json
    new_user = User(username=data["username"], email=data["email"], password_hash=data["password"])
    db.session.add(new_user)

    log_create = LogUser(IdLogType=1, IdTargetUser=new_user.id, IdAlterationBy=1, ActionDate=datetime.now())
    db.session.add(log_create)
    return jsonify({"message": "Usuário criado com sucesso"}), 201

@user_bp.route("/users/update/<int:id>", methods=["PUT"])
def update_user(id):
    data = request.json
    user = User.query.filter_by(id=id).first()
    if user:
        user.username = data["username"]
        user.email = data["email"]
        user.password_hash = data["password"]

        log_update = LogUser(IdLogType=2, IdTargetUser=user.id, IdAlterationBy=1, ActionDate=datetime.now())
        db.session.add(log_update)
        return jsonify({"message": "Usuário atualizado com sucesso"}), 200
    else:
        return jsonify({"message": "Usuário não encontrado"}), 404

@user_bp.route("/users/delete/<int:id>", methods=["DELETE"])
def delete_user(id):
    user = User.query.filter_by(id=id).first()
    if user:
        db.session.delete(user)

        log_delete = LogUser(IdLogType=3, IdTargetUser=user.id, IdAlterationBy=1, ActionDate=datetime.now())
        db.session.add(log_delete)
        return jsonify({"message": "Usuário excluído com sucesso"}), 200
    else:
        return jsonify({"message": "Usuário não encontrado"}), 404

@user_bp.route("/user/search/<int:id>", methods=["GET"], endpoint="search_user_by_id")
def search_user(id):
    search_user = User.query.filter_by(id=id).All()
    if search_user:
        return jsonify({"message": "Usuário encontrado"}), 200
    else:
        return jsonify({"message": "Usuário não encontrado"}), 404

@user_bp.route("/users/search", methods=["GET"], endpoint="search_all_users")
def search_users():
    search_users = User.query.all()
    if search_users:
        return jsonify({"message": "Usuários encontrados"}), 200
    else:
        return jsonify({"message": "Usuários não encontrados"}), 404
