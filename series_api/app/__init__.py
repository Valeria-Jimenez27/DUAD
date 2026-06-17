import os
from flask import Flask

try:
    from dotenv import load_dotenv
    load_dotenv()
except ImportError:
    pass


def create_app() -> Flask:
    app = Flask(__name__)
    app.config["DATABASE_URL"] = os.environ.get("DATABASE_URL", "")

    from app.routes import api_bp  # routes/__init__.py ya importa series.py

    app.register_blueprint(api_bp)

    return app
