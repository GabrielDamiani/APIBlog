from flask import Blueprint, request, jsonify
from ..DatabaseConnection import db
from ..Models.LogType import LogType
from ..Models.LogUsers import LogUser
from ..Models.Users import User
from datetime import datetime

user_bp = Blueprint("user_bp", __name__)

@user_bp.route("/users/create", methods=["POST"])
def create_user():
    data = request.get_json()
    print("JSON Data:", data)

    if not data or not data.get("username") or not data.get("email") or not data.get("password"):
        return jsonify({"message": "Dados inválidos. Favor fornecer 'username', 'email' e 'password'."}), 400
    
    new_user = User(Name=data["username"], Login=data["email"], Password=data["password"])
    db.session.add(new_user)
    db.session.commit()
    
    log_create = LogUser(IdLogType=1, IdTargetUser=new_user.Id, IdAlterationBy=1, ActionDate=datetime.now())
    db.session.add(log_create)
    db.session.commit()
    
    return jsonify({"message": "Usuário criado com sucesso"}), 201

@user_bp.route("/users/update/<int:id>", methods=["PUT"])
def update_user(id):
    data = request.json
    user = User.query.filter_by(Id=id).first()
    if user:
        user.Name = data["username"]
        user.Login = data["email"]
        user.Password = data["password"]

        log_update = LogUser(IdLogType=2, IdTargetUser=user.Id, IdAlterationBy=1, ActionDate=datetime.now())
        db.session.add(log_update)
        db.session.commit()

        return jsonify({"message": "Usuário atualizado com sucesso"}), 200
    else:
        return jsonify({"message": "Usuário não encontrado"}), 404

@user_bp.route("/users/delete/<int:id>", methods=["DELETE"])
def delete_user(id):
    user = User.query.filter_by(Id=id, Active=1).first()
    
    if user:
        user.Active = 0

        log_delete = LogUser(IdLogType=3, IdTargetUser=user.Id, IdAlterationBy=1, ActionDate=datetime.now())
        db.session.add(log_delete)
        db.session.commit()

        return jsonify({"message": "Usuário excluído com sucesso"}), 200
    else:
        return jsonify({"message": "Usuário não encontrado"}), 404


@user_bp.route("/users/search/<int:id>", methods=["GET"], endpoint="search_user")
def search_user(id):
    user = User.query.filter_by(Id=id, Active=1).first()

    if not user:
        return jsonify({"message": "Usuário não encontrado"}), 404

    user_data = {
        "Name": user.Name
    }

    return jsonify({"message": "Usuário encontrado", "user": user_data}), 200

@user_bp.route("/users/search", methods=["GET"], endpoint="search_all_users")
def search_users():
    users = User.query.filter_by(Active=1).all()

    if not users:
        return jsonify({"message": "Usuarios nao encontrados"}), 404

    users_list = [
        {
            "Name": user.Name
        }
        for user in users
    ]

    return jsonify({"message": "Usuarios encontrados", "users": users_list}), 200
