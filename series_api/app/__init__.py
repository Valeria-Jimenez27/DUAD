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

    # Importar rutas primero: esto registra los modelos en Base.metadata
    from app.routes import api_bp
    app.register_blueprint(api_bp)

    # create_all después: Base.metadata ya tiene todas las tablas
    from app.database import Base, engine
    if engine is not None:
        Base.metadata.create_all(engine)

    return app
