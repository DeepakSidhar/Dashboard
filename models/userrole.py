from . import db
import datetime

class UserRole(db.Model): # user class is a subclass of  db.Model
    __tablename__ = 'user_role'  # optional this is to id the table
    user_id = db.Column(db.Integer, db.ForeignKey("user.id"), primary_key=True)  # needs to e a forgnn key  and composite primary keyTODO
    role_id = db.Column(db.Integer, db.ForeignKey("role.id"), primary_key=True)  # needs to e a forgnn key and composite primary key TODO
    created_at = db.Column(db.DateTime, default=datetime.datetime.now(datetime.timezone.utc), nullable=False)
    updated_at = db.Column(db.DateTime, default=datetime.datetime.now(datetime.timezone.utc), nullable=False)

