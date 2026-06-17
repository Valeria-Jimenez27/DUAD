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
    @app.route("/")
    def index():
        from flask import jsonify
        return jsonify({
            "name": "Series API",
            "version": "1.0",
            "description": "API personal para trackear series de TV",
            "endpoints": {
                "series": "/api/v1/series",
                "series_detail": "/api/v1/series/<id>",
                "tracking": "/api/v1/series/<id>/tracking",
                "stats": "/api/v1/stats",
                "platforms": "/api/v1/platforms",
                "genres": "/api/v1/genres",
                "login": "/api/v1/auth/login",
            }
        })

    from app.routes import api_bp
    app.register_blueprint(api_bp)

    # create_all después: Base.metadata ya tiene todas las tablas
    from app.database import Base, engine
    if engine is not None:
        Base.metadata.create_all(engine)

    return app
