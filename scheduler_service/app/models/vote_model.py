from app.db.database import db
from datetime import datetime
import uuid
from sqlalchemy.dialects.mysql import CHAR

# Represents a single vote submitted by a participant for a specific poll
class Vote(db.Model):
    id = db.Column(CHAR(36), primary_key=True, default=lambda: str(uuid.uuid4()))
    # Many to one relationship with the poll model
    poll_id = db.Column(CHAR(36), db.ForeignKey('poll.id'), nullable=False)
    voter_email = db.Column(db.String(255), nullable=False)
    selected_dates = db.Column(db.Text, nullable=False)
    created_at = db.Column(db.DateTime, default=datetime.now)

    def to_dict(self):
        return {
            'id': self.id,
            'voter_email': self.voter_email,
            'selected_dates': self.selected_dates,
            'created_at': self.created_at.isoformat()
        }