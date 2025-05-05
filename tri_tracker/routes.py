from flask import render_template, request, jsonify, redirect, url_for, flash, session
from tri_tracker.models import User, Workout, db
import time


def init_routes(app):
    @app.route("/")
    def index():
        #users = User.query.all()
        username = session.get("username")
        user_id = session.get("user_id")
        if username and user_id:
            return render_template("index.html", username=username, user_id=user_id)    
        #return render_template("login.html", users=users)
        return redirect(url_for("login"))
    
    
    @app.route("/login", methods=["POST", "GET"])
    def login():
        if request.method == "POST":
            t0 = time.time()
            username = request.form.get("username")
            t1 = time.time()
            user = User.query.filter_by(username=username).first()
            t2 = time.time()
            
            session["username"] = username
            session["user_id"] = user.id
            t3 = time.time()

            print(f"Form read: {(t1 - t0):.4f}s")
            print(f"DB query: {(t2 - t1):.4f}s")
            print(f"Session set: {(t3 - t2):.4f}s")
            print(f"Total before redirect: {(t3 - t0):.4f}s")
            
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
    

def run_workouts() -> list[float]:
    run_workouts = db.session.query(Workout).filter(Workout.workout_type == "run").all()
    return [workout.pace for workout in run_workouts]


def swim_workouts() -> list[float]:
    swim_workouts = db.session.query(Workout).filter(Workout.workout_type == "swim").all()
    return [workout.pace for workout in swim_workouts]


def bike_workouts() -> list[float]:
    bike_workouts = db.session.query(Workout).filter(Workout.workout_type == "bike").all()
    return [workout.pace for workout in bike_workouts]