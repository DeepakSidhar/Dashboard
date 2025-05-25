from . import db
import datetime

class ProblemManagement(db.Model): # user class is a subclass of  db.Model
    __tablename__ = 'problem_management'  # optional this is to id the table
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(80), unique=True, nullable=False)
    description = db.Column(db.String(120), unique=True, nullable=False)
    status = db.Column(db.String(50), nullable=False)
    priority = db.Column(db.Integer,nullable=False)
    impact = db.Column(db.String(80), nullable=False)
    assignee_id = db.Column(db.Integer, db.ForeignKey("user.id"))  # needs to e a forgnn key TODO
    created_id = db.Column(db.Integer, db.ForeignKey("user.id"), nullable=False)
    root_cause = db.Column(db.String(80), nullable=False)
    resolution = db.Column(db.String(120), nullable=False)
    incident_id = db.Column(db.Integer, db.ForeignKey("incident_management.id"),nullable=False)  # needs to e a forgnn key TODO
    created_at = db.Column(db.DateTime, default=datetime.datetime.now(datetime.timezone.utc), nullable=False)
    updated_at = db.Column(db.DateTime, default=datetime.datetime.now(datetime.timezone.utc), nullable=False)

