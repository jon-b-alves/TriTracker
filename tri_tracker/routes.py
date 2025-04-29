from flask import render_template, request, jsonify
from tri_tracker.models import User, Workout, db

def init_routes(app):
    @app.route("/")
    def index():
        return render_template("index.html")

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