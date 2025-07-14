from . import db
import datetime

class IncidentManagement(db.Model): # user class is a subclass of  db.Model
    __tablename__ = 'incident_management'  # optional this is to id the table
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(80), nullable=False)
    description = db.Column(db.String(120),  nullable=False)
    status = db.Column(db.String(50), nullable=False)
    priority = db.Column(db.String(10), nullable=False)
    impact = db.Column(db.String(80),  nullable=False)
    assignee_id = db.Column(db.Integer, db.ForeignKey("user.id"))
    incident_type = db.Column(db.String(80),  nullable=False)
    software_id = db.Column(db.Integer, db.ForeignKey("software.id"))
    hardware_id = db.Column(db.Integer, db.ForeignKey("hardware.id"))
    reported_time = db.Column(db.DateTime, default=datetime.datetime.now(datetime.timezone.utc), nullable=False)
    resolved_time = db.Column(db.DateTime)
    created_at = db.Column(db.DateTime, default=datetime.datetime.now(datetime.timezone.utc), nullable=False)
    updated_at = db.Column(db.DateTime, default=datetime.datetime.now(datetime.timezone.utc), nullable=False)

    user = db.relationship('User')
    hardware = db.relationship('Hardware')
    software = db.relationship('Software')


