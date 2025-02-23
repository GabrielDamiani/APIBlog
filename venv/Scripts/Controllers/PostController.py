from flask import Blueprint, request, jsonify
from ..DatabaseConnection import db
from ..Models.Posts import Post
from ..Models.LogPosts import LogPost
from datetime import datetime
from ..Models.Users import User

post_bp = Blueprint("post_bp", __name__)

@post_bp.route("/posts/create", methods=["POST"])
def create_post():
    data = request.json
    new_post = Post(title=data["title"], content=data["content"], active=1)
    db.session.add(new_post)

    log_create = LogPost(IdLogType=1, IdTargetPost=new_post.id, IdAlterationBy=1, ActionDate=datetime.now())
    db.session.add(log_create)
    return jsonify({"message": "Post criado com sucesso"}), 201

@post_bp.route("/posts/update/<int:id>", methods=["PUT"])
def update_post(id):
    data = request.json
    post = Post.query.filter_by(id=id).first()
    if post:
        post.title = data["title"]
        post.content = data["content"]
        post.active = 1

        log_update = LogPost(IdLogType=2, IdTargetPost=post.id, IdAlterationBy=1, ActionDate=datetime.now())
        db.session.add(log_update)
        return jsonify({"message": "Post atualizado com sucesso"}), 200
    else:
        return jsonify({"message": "Post não encontrado"}), 404

@post_bp.route("/posts/delete/<int:id>", methods=["PUT"])
def delete_post(id):
    post = Post.query.filter_by(id=id).first()
    if post:
        db.session.delete(post)

        log_delete = LogPost(IdLogType=3, IdTargetPost=post.id, IdAlterationBy=1, ActionDate=datetime.now())
        db.session.add(log_delete)
        return jsonify({"message": "Post excluído com sucesso"}), 200
    else:
        return jsonify({"message": "Post não encontrado"}), 404
    
def delete_post(id):
    post = Post.query.filter_by(id=id).first()
    if post:
        post.active = 0

        log_delete = LogPost(IdLogType=3, IdTargetPost=post.id, IdAlterationBy=1, ActionDate=datetime.now())
        db.session.add(log_delete)
        return jsonify({"message": "Post atualizado com sucesso"}), 200
    else:
        return jsonify({"message": "Post não encontrado"}), 404

@post_bp.route("/posts/search/<int:id>", methods=["GET"], endpoint="search_all_posts") #Colocar o Id da pessoa no resultado
def search_post(id):
    search_post = Post.query.filter_by(id=id).All()
    if search_post:
        return jsonify({"message": "Post encontrado"}), 200
    else:
        return jsonify({"message": "Post não encontrado"}), 404

@post_bp.route("/posts/search/<int:id>", methods=["GET"], endpoint="search_post_by_id")
def search_post(id):
    search_post = db.session.query(
        Post.id, 
        Post.content, 
        Post.created_at, 
        User.id.label("author_id"), 
        User.username.label("author_name")
    ).join(User, Post.user_id == User.id).filter(Post.id == id).first()

    if search_post:
        return jsonify({
            "id": search_post.id,
            "content": search_post.content,
            "created_at": search_post.created_at,
            "author": {
                "id": search_post.author_id,
                "name": search_post.author_name
            }
        }), 200
    else:
        return jsonify({"message": "Post não encontrado"}), 404
