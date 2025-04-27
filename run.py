from tri_tracker import create_app

app = create_app()

if __name__ == "__main__":
    with app.app_context():
        # Create database tables if they don't exist
        from tri_tracker.models import db
        db.create_all()
    app.run(debug=True)
