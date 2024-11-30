from datetime import datetime
from werkzeug.security import generate_password_hash, check_password_hash
from flask_login import UserMixin
from app import db, login_manager

class User(UserMixin, db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(64), unique=True, nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    password_hash = db.Column(db.String(128))
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    points = db.Column(db.Integer, default=0)
    level = db.Column(db.Integer, default=1)
    
    # Relationships
    activities = db.relationship('Activity', backref='user', lazy='dynamic')
    challenges = db.relationship('UserChallenge', backref='user', lazy='dynamic')
    forum_posts = db.relationship('ForumPost', backref='author', lazy='dynamic')
    product_reviews = db.relationship('ProductReview', backref='author', lazy='dynamic')
    
    def set_password(self, password):
        self.password_hash = generate_password_hash(password)
    
    def check_password(self, password):
        return check_password_hash(self.password_hash, password)
    
    def add_points(self, points):
        self.points += points
        self.update_level()
        
    def update_level(self):
        self.level = (self.points // 1000) + 1

@login_manager.user_loader
def load_user(id):
    return User.query.get(int(id))
