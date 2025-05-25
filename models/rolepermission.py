from . import db
import datetime

class RolePermission(db.Model): # user class is a subclass of  db.Model
    __tablename__ = 'role_permission'  # optional this is to id the table
    role_id = db.Column(db.Integer, db.ForeignKey("role.id"), primary_key=True, ) # needs to e a forgnn key and  (composite primary key)
    permission_id = db.Column(db.Integer, db.ForeignKey("permission.id"), primary_key=True) # needs to e a forgnn key and  (composite primary key)
    created_at = db.Column(db.DateTime, default=datetime.datetime.now(datetime.timezone.utc), nullable=False)
    updated_at = db.Column(db.DateTime, default=datetime.datetime.now(datetime.timezone.utc), nullable=False)

