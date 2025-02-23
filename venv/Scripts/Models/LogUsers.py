from ..DatabaseConnection import db

class LogUser(db.Model):
    __tablename__ = 'LogUsers'
    Id = db.Column(db.BigInteger, primary_key=True, autoincrement=True)
    IdLogType = db.Column(db.SmallInteger, db.ForeignKey('LogType.Id'), nullable=False)
    IdTargetUser = db.Column(db.Integer, db.ForeignKey('Users.Id'), nullable=False)
    IdAlterationBy = db.Column(db.Integer, db.ForeignKey('Users.Id'), nullable=False)
    ActionDate = db.Column(db.Date, nullable=False)

    log_type = db.relationship('LogType', backref='log_users')
    target_user = db.relationship('User', foreign_keys=[IdTargetUser], backref='target_log_users')
    alteration_by = db.relationship('User', foreign_keys=[IdAlterationBy], backref='alteration_log_users')
