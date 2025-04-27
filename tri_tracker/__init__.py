from flask import Flask
from tri_tracker.models import db

def create_app():
    app = Flask(__name__)
    app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///tri_tracker.db"
    app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
    db.init_app(app) # link db with flask app
    from tri_tracker.routes import init_routes
    init_routes(app)
    return app
