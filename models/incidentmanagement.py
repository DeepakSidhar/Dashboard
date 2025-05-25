from . import db
import datetime

class IncidentManagement(db.Model): # user class is a subclass of  db.Model
    __tablename__ = 'incident_management'  # optional this is to id the table
    id = db.Column(db.Integer, primary_key=True)# needs to e a forgnn key TODO
    title = db.Column(db.String(80), nullable=False)
    description = db.Column(db.String(120),  nullable=False)
    status = db.Column(db.String(50), nullable=False)
    priority = db.Column(db.Integer, nullable=False)
    impact = db.Column(db.String(80),  nullable=False)
    assignee_id = db.Column(db.Integer, db.ForeignKey("user.id"))  # needs to e a forgnn key TODO
    incident_type = db.Column(db.String(80),  nullable=False)
    software_id = db.Column(db.Integer, db.ForeignKey("software.id"))  # needs to e a forgnn key TODO
    hardware_id = db.Column(db.Integer, db.ForeignKey("hardware.id"))  # needs to e a forgnn key TODO
    reported_time = db.Column(db.DateTime, default=datetime.datetime.now(datetime.timezone.utc), nullable=False)
    resolved_time = db.Column(db.DateTime, default=datetime.datetime.now(datetime.timezone.utc), nullable=False)
    created_at = db.Column(db.DateTime, default=datetime.datetime.now(datetime.timezone.utc), nullable=False)
    updated_at = db.Column(db.DateTime, default=datetime.datetime.now(datetime.timezone.utc), nullable=False)

