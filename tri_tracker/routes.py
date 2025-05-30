from flask import render_template, request, jsonify, redirect, url_for, flash, session
from tri_tracker.models import User, Workout, db
from sqlalchemy import asc, desc, func
import time


def init_routes(app):
    @app.route("/")
    def index():
        username = session.get("username")
        user_id = session.get("user_id")

        run_workout_dates, run_workout_paces, run_workout_average_pace = get_workouts("run", user_id)
        swim_workout_dates, swim_workout_paces, swim_workout_average_pace = get_workouts("swim", user_id)
        bike_workout_dates, bike_workout_paces, bike_workout_average_pace = get_workouts("bike", user_id)
        doughnut_labels, doughnut_distances, doughnut_durations = get_totals_by_type(user_id)
        

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
                bike_workout_average_pace=bike_workout_average_pace,

                doughnut_labels=doughnut_labels, 
                doughnut_distances=doughnut_distances, 
                doughnut_durations=doughnut_durations
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
        session.pop("user_id", None)
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


    @app.route("/workout-log", methods=["GET"])
    def workout_log():
        user_id = session.get("user_id")
        workouts = get_log(user_id)
        return render_template("workout-log.html", workouts=workouts)
    

    @app.route("/delete-workout/<int:workout_id>", methods=["POST"])
    def delete_workout(workout_id):
        workout = Workout.query.get_or_404(workout_id)
        db.session.delete(workout)
        db.session.commit()
        return redirect(url_for("workout_log"))


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
    workouts = db.session.query(Workout.workout_type, Workout.duration, Workout.distance, Workout.pace, Workout.date, Workout.id)\
    .filter_by(user_id=user_id)\
    .order_by(desc(Workout.date))\
    .all()

    return workouts

def get_totals_by_type(user_id: int):
    results = db.session.query(
        Workout.workout_type,
        func.sum(Workout.distance).label("total_distance"),
        func.sum(Workout.duration).label("total_duration"),
    )\
    .filter_by(user_id=user_id)\
    .group_by(Workout.workout_type)\
    .all()

    labels = []
    distances = []
    durations = []

    for workout_type, total_distance, total_duration in results:
        labels.append(workout_type)
        distances.append(total_distance or 0)
        durations.append(total_duration or 0)

    return labels, distances, durations