from . import db
import datetime

class Software(db.Model): # user class is a subclass of  db.Model
    __tablename__ = 'software'  # optional this is to id the table
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(80), unique=True, nullable=False)
    version = db.Column(db.String(120), unique=True, nullable=False)
    vendor = db.Column(db.String(80), unique=True, nullable=False)
    model  = db.Column(db.String(80),  nullable=False)
    hardware_id = db.Column(db.Integer, db.ForeignKey("hardware.id"), nullable=False) # needs to e a forgnn key TODO
    status = db.Column(db.String(50), nullable=False)
    installation_date = db.Column(db.DateTime, default=datetime.datetime.now(datetime.timezone.utc), nullable=False)
    licence_expiry_date = db.Column(db.DateTime, default=datetime.datetime.now(datetime.timezone.utc), nullable=False)
    created_at = db.Column(db.DateTime, default=datetime.datetime.now(datetime.timezone.utc), nullable=False)
    updated_at = db.Column(db.DateTime, default=datetime.datetime.now(datetime.timezone.utc), nullable=False)

