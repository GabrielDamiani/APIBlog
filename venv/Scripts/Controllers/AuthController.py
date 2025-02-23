# from flask import request, jsonify
# import jwt
# import datetime
# from werkzeug.security import check_password_hash
# from main import app
# from ..DatabaseConnection import db
# from ..Models.Users import User
# from functools import wraps

# @app.route("/login", methods=["POST"])
# def login():
#     data = request.get_json()
#     username = data.get('username')
#     password = data.get('password')

#     user = User.query.filter_by(username=username).first()

#     if user and check_password_hash(user.password, password):
#         token = jwt.encode({'user_id': user.id, 'exp': datetime.datetime.utcnow() + datetime.timedelta(hours=1)}, app.config['SECRET_KEY'], algorithm='HS256')
#         return jsonify({'token': token}), 200
#     else:
#         return jsonify({"message": "Invalid credentials"}), 401



# ##AINDA NÃO FAÇO IDEIA DO QUE É ENTAO CUIDADO



# # from functools import wraps
# # from flask import request, jsonify
# # import jwt
# # from your_app import app
# # from your_app.models import User

# def token_required(f):
#     @wraps(f)
#     def decorated_function(*args, **kwargs):
#         token = None
#         if 'Authorization' in request.headers:
#             token = request.headers['Authorization'].split(" ")[1]

#         if not token:
#             return jsonify({'message': 'Token is missing!'}), 401

#         try:
#             data = jwt.decode(token, app.config['SECRET_KEY'], algorithms=['HS256'])
#             current_user = User.query.get(data['user_id'])
#         except:
#             return jsonify({'message': 'Token is invalid!'}), 401

#         return f(current_user, *args, **kwargs)
#     return decorated_function
