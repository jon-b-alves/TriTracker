from flask import render_template, request, jsonify, redirect, url_for, flash
from tri_tracker.models import User, Workout, db

def init_routes(app):
    @app.route("/")
    def index():
        users = User.query.all()
        return render_template("index.html", users=users)

    @app.route("/user/<int:user_id>", methods=["GET"])
    def get_user(user_id):
        user = User.query.get(user_id)
        return jsonify({"username": user.username})
    
    @app.route("/test", methods=["POST"])
    def test():
        data = request.get_json()
        new_user = User(username=data["username"])
        db.session.add(new_user)
        db.session.commit()
        return jsonify({"message": "User created successfully!"}), 201
    
    @app.route("/login", methods=["POST"])
    def login():
        x=1
    

    @app.route("/create-user", methods=["POST"])
    def create_user():
        username = request.form.get("new_username").lower()

        existing_user = User.query.filter_by(username=username).first()
        if existing_user:
            flash("username already exists")
            return redirect(url_for("index"))
            
        db.session.add(User(username=username))
        db.session.commit()
        flash("user created successfully")
        return redirect(url_for("index"))
