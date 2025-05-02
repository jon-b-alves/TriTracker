from flask import render_template, request, jsonify, redirect, url_for, flash, session
from tri_tracker.models import User, Workout, db

def init_routes(app):
    @app.route("/")
    def index():
        users = User.query.all()
        username = session.get("username")
        if username:
            return render_template("index.html", username=username)    
        return render_template("login.html", users=users)
    
    
    @app.route("/login", methods=["POST", "GET"])
    def login():
        if request.method == "POST":
            username = request.form.get("username")
            session["username"] = username
            return redirect(url_for("index"))
        users = User.query.all()
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
        user = User.query.filter_by(username=session["username"]).first()

        workout = Workout(
            user=user,
            workout_type=workout_type,
            distance=float(distance),
            duration=float(duration)
        )
        
        db.session.add(workout)
        db.session.commit()
        return redirect(url_for("index"))