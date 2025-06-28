from . import db
import datetime

class Hardware(db.Model): # user class is a subclass of  db.Model
    __tablename__ = 'hardware'  # optional this is to id the table
    id = db.Column(db.Integer, primary_key=True)# needs to e a forgnn key TODO
    name = db.Column(db.String(80), unique=True, nullable=False)
    type = db.Column(db.String(120), nullable=False)
    manufacturer = db.Column(db.String(80),  nullable=False)
    model  = db.Column(db.String(80),  nullable=False)
    location = db.Column(db.String(80),  nullable=False)
    status = db.Column(db.String(50), nullable=False)
    purchase_date = db.Column(db.DateTime, default=datetime.datetime.now(datetime.timezone.utc), nullable=False)
    created_at = db.Column(db.DateTime, default=datetime.datetime.now(datetime.timezone.utc), nullable=False)
    updated_at = db.Column(db.DateTime, default=datetime.datetime.now(datetime.timezone.utc), nullable=False)