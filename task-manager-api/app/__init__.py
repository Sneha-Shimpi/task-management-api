from flask import Flask, jsonify, render_template
from sqlalchemy import text
from sqlalchemy.exc import OperationalError

from app.config import config_by_name
from app.extensions import db


def ensure_database_schema(app):
    with app.app_context():
        inspector = db.inspect(db.engine)
        tables = inspector.get_table_names()

        if "tasks" not in tables:
            db.create_all()
            return

        columns = [column["name"] for column in inspector.get_columns("tasks")]
        if "due_date" not in columns:
            try:
                db.session.execute(text("ALTER TABLE tasks ADD COLUMN due_date DATE"))
                db.session.commit()
            except OperationalError as exc:
                db.session.rollback()
                if "duplicate column name" not in str(exc).lower() and "already exists" not in str(exc).lower():
                    raise


def create_app(config_name="development"):
    app = Flask(__name__)
    app.config.from_object(config_by_name[config_name])

    db.init_app(app)

    from app.routes import api

    app.register_blueprint(api)

    @app.route("/", methods=["GET"])
    def index():
        return render_template("index.html")

    @app.route("/health", methods=["GET"])
    def health():
        return jsonify({"status": "ok"})

    @app.errorhandler(404)
    def not_found(e):
        return jsonify({"error": "Resource not found"}), 404

    @app.errorhandler(405)
    def method_not_allowed(e):
        return jsonify({"error": "Method not allowed"}), 405

    @app.errorhandler(500)
    def internal_error(e):
        db.session.rollback()
        return jsonify({"error": "Internal server error"}), 500

    ensure_database_schema(app)

    return app
