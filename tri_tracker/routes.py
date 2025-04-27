from flask import render_template, request, jsonify
from tri_tracker.models import User, Workout, db

def init_routes(app):
    @app.route("/")
    def index():
        render_template("index.html")

    @app.route("/submit", methods=["POST"])
    def submit():
        name = request.form["name"]
        return f"Name: {name}"