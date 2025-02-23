from ..DatabaseConnection import db

class Post(db.Model):
    __tablename__ = 'Posts'
    Id = db.Column(db.BigInteger, primary_key=True, autoincrement=True)
    Title = db.Column(db.String(100), nullable=False)
    Content = db.Column(db.String(300), nullable=False)
    Active = db.Column(db.Boolean, default=True)
