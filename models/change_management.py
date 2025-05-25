from . import db
import datetime

class ChangeManagement(db.Model): # user class is a subclass of  db.Model
    __tablename__ = 'change_management'  # optional this is to id the table
    id = db.Column(db.Integer, primary_key=True)# needs to e a forgnn key TODO
    title = db.Column(db.String(80), nullable=False)
    description = db.Column(db.String(120), nullable=False)
    status = db.Column(db.String(50), nullable=False)
    priority = db.Column(db.Integer, nullable=False)
    impact = db.Column(db.String(80),  nullable=False)
    change_type = db.Column(db.String(80), nullable=False)
    requested_by_id = db.Column(db.Integer, db.ForeignKey("user.id"), nullable=False)  # needs to e a forgnn key TODO
    proposed_time = db.Column(db.DateTime, default=datetime.datetime.now(datetime.timezone.utc), nullable=False)
    executed_time = db.Column(db.DateTime, default=datetime.datetime.now(datetime.timezone.utc), nullable=False)
    software_id = db.Column(db.Integer, db.ForeignKey("software.id"), nullable=False)#  # needs to e a forgnn key TODO
    hardware_id = db.Column(db.Integer, db.ForeignKey("hardware.id"), nullable=False)# # needs to e a forgnn key TODO
    created_at = db.Column(db.DateTime, default=datetime.datetime.now(datetime.timezone.utc), nullable=False)
    updated_at = db.Column(db.DateTime, default=datetime.datetime.now(datetime.timezone.utc), nullable=False)


