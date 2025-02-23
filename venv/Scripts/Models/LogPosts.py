from ..DatabaseConnection import db

class LogPost(db.Model):
    __tablename__ = 'LogPosts'
    Id = db.Column(db.BigInteger, primary_key=True, autoincrement=True)
    IdLogType = db.Column(db.SmallInteger, db.ForeignKey('LogType.Id'), nullable=False)
    IdTargetPost = db.Column(db.BigInteger, db.ForeignKey('Posts.Id'), nullable=False)
    IdAlterationBy = db.Column(db.Integer, db.ForeignKey('Users.Id'), nullable=False)
    ActionDate = db.Column(db.Date, nullable=False)

    log_type = db.relationship('LogType', backref='log_posts')
    target_post = db.relationship('Post', backref='log_posts')
    alteration_by = db.relationship('User', backref='log_posts')

    # coisas que podem ser feitas e me deixarem feliz: carro novo, carro novo, carro novo
