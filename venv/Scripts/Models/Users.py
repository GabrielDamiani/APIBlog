from ..DatabaseConnection import db

class User(db.Model): 
    __tablename__ = 'Users'
    Id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    Name = db.Column(db.String(100), nullable=False)
    Login = db.Column(db.String(100), nullable=False, unique=True)
    Password = db.Column(db.String(255), nullable=False)
    Admin = db.Column(db.Boolean, default=False)
    Active = db.Column(db.Boolean, default=True)
