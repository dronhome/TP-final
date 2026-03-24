import os
from flask import Flask


def create_app():
    app = Flask(__name__)

    # Ensure the exercises directory exists on startup
    exercises_dir = os.environ.get("EXERCISES_DIR", "/exercises")
    os.makedirs(exercises_dir, exist_ok=True)

    from .routes.health import health_bp
    from .routes.exercise import exercise_bp
    app.register_blueprint(health_bp)
    app.register_blueprint(exercise_bp)

    return app