from flask_sqlalchemy import SQLAlchemy
from datetime import datetime

# Initialize Flask-SQLAlchemy (to be set in Flask app)
db = SQLAlchemy()

class User(db.Model):
    __tablename__ = "users"

    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String, nullable=False, unique=True)
    workouts = db.relationship("Workout", back_populates="user", cascade="all, delete-orphan")

class Workout(db.Model):
    __tablename__ = "workouts"

    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey("users.id"), nullable=False)
    workout_type = db.Column(db.String, nullable=False)  # Swim, Bike, Run
    duration = db.Column(db.Float, nullable=False)  # Minutes
    distance = db.Column(db.Float, nullable=False)  # Kilometers
    date = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)
    user = db.relationship("User", back_populates="workouts")