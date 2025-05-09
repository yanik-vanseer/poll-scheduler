from app.db.database import db
from datetime import datetime
import uuid
from sqlalchemy.dialects.mysql import CHAR

# Represents a poll created by an organiser with a list of invited emails and available dates.
class Poll(db.Model):
    id = db.Column(CHAR(36), primary_key=True, default=lambda: str(uuid.uuid4()))
    organiser = db.Column(db.String(120), nullable=False)
    invited_emails = db.Column(db.Text, nullable=False)
    available_dates = db.Column(db.Text, nullable=False)
    # One to many relationship with the voting model
    votes = db.relationship('Vote', backref='poll', lazy=True, cascade="all, delete-orphan")
    created_at = db.Column(db.DateTime, default=datetime.now)

    def to_dict(self):
        return {
            'id': self.id,
            'organiser': self.organiser,
            'invited_emails': self.invited_emails,
            'available_dates': self.available_dates,
            'created_at': self.created_at.isoformat(),
            'votes': [vote.to_dict() for vote in self.votes]
        }