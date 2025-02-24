from flask import Blueprint, request, jsonify
from datetime import datetime

from ..DatabaseConnection import db
from ..Models.LogType import LogType
from ..Models.LogUsers import LogUser
from ..Models.Users import User
from ..Controllers.AuthController import token_required
from ..Models.Posts import Post
from ..Models.LogPosts import LogPost

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
    
    log_create = LogUser(IdLogType=1, IdTargetUser=new_user.Id, IdAlterationBy=new_user.Id, ActionDate=datetime.now())
    db.session.add(log_create)
    db.session.commit()
    
    return jsonify({"message": "Usuário criado com sucesso"}), 201

@user_bp.route("/users/update/<int:id>", methods=["PUT"])
@token_required
def update_user(current_user, id):
    data = request.json
    user = User.query.filter_by(Id=id).first()

    if user:
        if current_user.Id == user.Id or current_user.Admin == 1:
            user.Name = data.get("username")
            user.Login = data.get("email")
            user.Password = data.get("password")

            log_update = LogUser(IdLogType=2, IdTargetUser=user.Id, IdAlterationBy=current_user.Id, ActionDate=datetime.now())
            db.session.add(log_update)
            db.session.commit()

            return jsonify({"Mensagem": "Usuario atualizado com sucesso"}), 200
        else:
            return jsonify({"Mensagem": "Permissao negada. Somente o usuario ou um administrador podem realizar esta açao."}), 403
    else:
        return jsonify({"Mensagem": "Usuario nao encontrado"}), 404


@user_bp.route("/users/delete/<int:id>", methods=["DELETE"])
@token_required
def delete_user(current_user, id):
    user = User.query.filter_by(Id=id, Active=1).first()
    
    if user:
        if current_user.Id == user.Id or current_user.Admin == 1:
            user.Active = 0
            
            posts = Post.query.filter_by(IdCreator=id, Active=1).all()
            for post in posts:
                post.Active = 0
                log_delete_post = LogPost(IdLogType=3, IdTargetPost=post.Id, IdAlterationBy=current_user.Id, ActionDate=datetime.now())
                db.session.add(log_delete_post)

            log_delete_user = LogUser(IdLogType=3, IdTargetUser=user.Id, IdAlterationBy=current_user.Id, ActionDate=datetime.now())
            db.session.add(log_delete_user)

            db.session.commit()

            return jsonify({"Mensagem": "Usuario e seus posts excluidos com sucesso"}), 200
        else:
            return jsonify({"Mensagem": "Permissao negada"}), 403
    else:
        return jsonify({"Mensagem": "Usuario não encontrado"}), 404

@user_bp.route("/users/search/<int:id>", methods=["GET"], endpoint="search_user")
@token_required
def search_user(id):
    user = User.query.filter_by(Id=id, Active=1).first()

    if not user:
        return jsonify({"message": "Usuário não encontrado"}), 404

    user_data = {
        "Name": user.Name
    }

    return jsonify({"message": "Usuário encontrado", "user": user_data}), 200

@user_bp.route("/users/search", methods=["GET"], endpoint="search_all_users")
@token_required
def search_users(current_user):
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
