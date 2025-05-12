from flask import render_template, request, jsonify, redirect, url_for, flash, session
from tri_tracker.models import User, Workout, db
from sqlalchemy import asc
import time


def init_routes(app):
    @app.route("/")
    def index():
        username = session.get("username")
        user_id = session.get("user_id")

        run_workout_dates, run_workout_paces, run_workout_average_pace = get_workouts("run", user_id)
        swim_workout_dates, swim_workout_paces, swim_workout_average_pace = get_workouts("swim", user_id)
        bike_workout_dates, bike_workout_paces, bike_workout_average_pace = get_workouts("bike", user_id)
        

        if username and user_id:
            return render_template(
                "index.html", 
                username=username, 
                user_id=user_id,
                
                run_workout_dates=run_workout_dates, 
                run_workout_paces=run_workout_paces,
                run_workout_average_pace=run_workout_average_pace,
                
                swim_workout_dates=swim_workout_dates, 
                swim_workout_paces=swim_workout_paces,
                swim_workout_average_pace=swim_workout_average_pace,
                
                bike_workout_dates=bike_workout_dates,
                bike_workout_paces=bike_workout_paces,
                bike_workout_average_pace=bike_workout_average_pace
            )    
        return redirect(url_for("login"))
    
    
    @app.route("/login", methods=["POST", "GET"])
    def login():
        if request.method == "POST":
            username = request.form.get("username")
            user = User.query.filter_by(username=username).first()
            
            session["username"] = username
            session["user_id"] = user.id
            
            return redirect(url_for("index"))
        
        users = User.query.with_entities(User.username).all()
        return render_template("login.html", users=users)
    

    @app.route("/logout")
    def logout():
        session.pop("username", None)
        return redirect(url_for("login"))

    
    @app.route("/create-user", methods=["POST"])
    def create_user():
        username = request.form.get("new_username").lower()

        existing_user = User.query.filter_by(username=username).first()
        if existing_user:
            flash("username already exists")
            return redirect(url_for("login"))
            
        db.session.add(User(username=username))
        db.session.commit()
        flash("user created successfully")
        return redirect(url_for("login"))


    @app.route("/create-workout", methods=["POST"])
    def create_workout():
        workout_type = request.form.get("type")
        distance = request.form.get("distance")
        duration = request.form.get("duration")
        pace = float(duration) / float(distance)         
        user = User.query.filter_by(username=session["username"]).first()

        workout = Workout(
            user=user,
            workout_type=workout_type,
            distance=float(distance),
            duration=float(duration),
            pace=float(pace)
        )
        
        db.session.add(workout)
        db.session.commit()
        return redirect(url_for("index"))
    

def get_workouts(workout_type: str, user_id: int):
    workouts = db.session.query(Workout.date, Workout.pace)\
    .filter_by(user_id=user_id, workout_type=workout_type)\
    .order_by(asc(Workout.date))\
    .all()

    dates = [workout.date.strftime("%m/%d") for workout in workouts]
    paces = [workout.pace for workout in workouts]
    average_pace = sum(paces) / len(paces) if paces else 0
    average_pace_line = [average_pace] * len(dates)
    
    return dates, paces, average_pace_line

def get_log(user_id: int):
    workouts = db.session.query(Workout.workout_type, Workout.duration, Workout.distance, Workout.pace, Workout.date)\
    .filter_by(user_id=user_id)\
    .order_by(asc(Workout.date))\
    .all()