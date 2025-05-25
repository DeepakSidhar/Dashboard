from . import db
import datetime

class User(db.Model): # user class is a subclass of  db.Model
    __tablename__ = 'user' # optional this is to id the table
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(80), unique=True, nullable=False)
    password = db.Column(db.String(120), unique=True, nullable=False)
    email_text = db.Column(db.String(80), unique=True, nullable=False)
    first_name  = db.Column(db.String(80),  nullable=False)
    last_name = db.Column(db.String(80),  nullable=False)
    #role = db.Column(db.String(50), db.ForeignKey("role.id"), nullable=False) # removes roled once  class diagram is implemented
    created_at = db.Column(db.DateTime, default=datetime.datetime.now(datetime.timezone.utc), nullable=False)
    updated_at = db.Column(db.DateTime, default=datetime.datetime.now(datetime.timezone.utc), nullable=False)
