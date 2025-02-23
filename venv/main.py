from flask import Flask
from Scripts.DatabaseConnection import SQLALCHEMY_DATABASE_URI, db

app = Flask(__name__)
app.config["SECRET_KEY"] = "secret"

app.config["SQLALCHEMY_DATABASE_URI"] = SQLALCHEMY_DATABASE_URI
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False

db.init_app(app)

from Scripts.Controllers.AuthController import login_bp
from Scripts.Controllers.UserController import user_bp
from Scripts.Controllers.PostController import post_bp

app.register_blueprint(login_bp)
app.register_blueprint(user_bp)
app.register_blueprint(post_bp)

if __name__ == "__main__":
    app.run(debug=True)
