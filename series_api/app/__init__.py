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

    # Crear tablas al arrancar (válido para este proyecto sin migraciones)
    from app.database import Base, engine
    if engine is not None:
        Base.metadata.create_all(engine)

    from app.routes import api_bp  # routes/__init__.py ya importa series.py
    app.register_blueprint(api_bp)

    return app
