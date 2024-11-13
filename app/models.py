from app import db
from datetime import datetime

class Case(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    age = db.Column(db.Integer, nullable=False)
    gender = db.Column(db.String(20), nullable=False)
    event_location = db.Column(db.String(100), nullable=False)
    traumatic_event = db.Column(db.String(200), nullable=False)
    scenario = db.Column(db.String(200), nullable=False)
    openness = db.Column(db.Integer, nullable=False)
    conscientiousness = db.Column(db.Integer, nullable=False)
    extraversion = db.Column(db.Integer, nullable=False)
    agreeableness = db.Column(db.Integer, nullable=False)
    neuroticism = db.Column(db.Integer, nullable=False)
    additional_features = db.Column(db.Text, nullable=True)
    improvise = db.Column(db.Boolean, default=False)
    narrative = db.Column(db.Text, nullable=True)
    timestamp = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)

    def __repr__(self):
        return f"Case('{self.name}', '{self.traumatic_event}', '{self.timestamp}')"