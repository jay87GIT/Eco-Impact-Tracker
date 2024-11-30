from datetime import datetime
from app import db

class Challenge(db.Model):
    __table_args__ = {'extend_existing': True}
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(100), nullable=False)
    description = db.Column(db.Text, nullable=False)
    points = db.Column(db.Integer, nullable=False)
    start_date = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)
    end_date = db.Column(db.DateTime, nullable=False)
    category = db.Column(db.String(50), nullable=False)
    difficulty = db.Column(db.String(20), nullable=False, default='medium')
    created_at = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)
    
    # Relationships
    participants = db.relationship('UserChallenge', backref='challenge', lazy='dynamic')
    
    def __repr__(self):
        return f'<Challenge {self.title}>'
    
    @property
    def active_participants_count(self):
        return self.participants.filter_by(completed=False).count()
    
    @property
    def completed_participants_count(self):
        return self.participants.filter_by(completed=True).count()
    
    @property
    def is_active(self):
        now = datetime.utcnow()
        return self.start_date <= now <= self.end_date

class UserChallenge(db.Model):
    __table_args__ = {'extend_existing': True}
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    challenge_id = db.Column(db.Integer, db.ForeignKey('challenge.id'), nullable=False)
    joined_at = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)
    completed = db.Column(db.Boolean, default=False)
    completed_at = db.Column(db.DateTime)
    
    def complete_challenge(self):
        if not self.completed:
            self.completed = True
            self.completed_at = datetime.utcnow()
            self.user.add_points(self.challenge.points)
            db.session.commit()
