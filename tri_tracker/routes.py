from flask import render_template, request, jsonify
from models import User, Workout
from tri_tracker import db, app