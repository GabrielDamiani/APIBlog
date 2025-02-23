from flask import Blueprint, request, jsonify
from datetime import datetime

from ..DatabaseConnection import db
from ..Models.Posts import Post
from ..Models.LogPosts import LogPost
from ..Models.Users import User
from ..Controllers.AuthController import token_required

post_bp = Blueprint("post_bp", __name__)

@post_bp.route("/posts/create", methods=["POST"])
@token_required
def create_post():
    data = request.json
    new_post = Post(Title=data["title"], Content=data["content"], IdCreator=data["author_id"], Active=1)
    db.session.add(new_post)
    db.session.commit()

    log_create = LogPost(IdLogType=1, IdTargetPost=new_post.Id, IdAlterationBy=new_post.IdCreator, ActionDate=datetime.now())
    db.session.add(log_create)
    db.session.commit()
    return jsonify({"message": "Post criado com sucesso"}), 201

@post_bp.route("/posts/update/<int:id>", methods=["PUT"])
@token_required
def update_post(id):
    data = request.json
    post = Post.query.filter_by(Id=id).first()
    if post:
        post.Title = data["title"]
        post.Content = data["content"]
        post.Active = 1
        db.session.commit()

        log_update = LogPost(IdLogType=2, IdTargetPost=post.Id, IdAlterationBy=1, ActionDate=datetime.now())
        print('o log é o id do post:', log_update)
        db.session.add(log_update)
        db.session.commit()
        return jsonify({"message": "Post atualizado com sucesso"}), 200
    else:
        return jsonify({"message": "Post não encontrado"}), 404

@post_bp.route("/posts/delete/<int:id>", methods=["DELETE"])
@token_required
def delete_post(id):
    post = Post.query.filter_by(Id=id).first()
    if post:
        post.Active = 0
        db.session.commit()

        log_delete = LogPost(IdLogType=3, IdTargetPost=post.Id, IdAlterationBy=1, ActionDate=datetime.now())
        db.session.add(log_delete)
        db.session.commit()
        return jsonify({"message": "Post deletado com sucesso"}), 200
    else:
        return jsonify({"message": "Post não encontrado"}), 404

@post_bp.route("/posts/search/<int:id>", methods=["GET"], endpoint="search_post_by_id")
@token_required
def search_post(id):
    post = Post.query.filter_by(Id=id, Active=1).first()

    if not post:
        return jsonify({"message": "Post não encontrado"}), 404

    post_data = {
        "Tile": post.Title,
        "Content": post.Content
    }

    return jsonify({"message": "Usuário encontrado", "post": post_data}), 200
    
@post_bp.route("/posts/search", methods=["GET"], endpoint="search_all_posts")
@token_required
def search_post():
    search_posts = db.session.query(
        Post.Id,
        Post.Title,
        Post.Content,
        User.Id.label("author_id"),
        User.Name.label("author_name")
    ).join(User, Post.IdCreator == User.Id).all()

    if search_posts:
        result = []
        for post in search_posts:
            result.append({
                "id": post.Id,
                "title": post.Title,
                "content": post.Content,
                "author": {
                    "id": post.author_id,
                    "name": post.author_name
                }
            })
        return jsonify(result), 200
    else:
        return jsonify({"message": "Post não encontrado"}), 404

@post_bp.route("/posts/search/by/user/<int:id>", methods=["GET"], endpoint="search_all_posts_by_user")
@token_required
def search_post(id):
    search_posts = db.session.query(Post).filter(Post.IdCreator == id).all()

    if search_posts:
        result = []
        for post in search_posts:
            result.append({
                "id": post.Id,
                "title": post.Title,
                "content": post.Content
            })
        return jsonify(result), 200
    else:
        return jsonify({"message": "Post não encontrado"}), 404

