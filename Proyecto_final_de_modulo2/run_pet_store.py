from dotenv import load_dotenv

load_dotenv()

from flask import Flask
from flask_cors import CORS

from app.routes.users import users_bp
from app.routes.products import products_bp
from app.routes.customers import customers_bp
from app.routes.sales import sales_bp

from app.database.engine import create_tables


app = Flask(__name__)


# ============================================================
# CORS
# ============================================================
# Permite que el frontend ejecutado mediante Live Server
# pueda comunicarse con Flask.
#
# Live Server normalmente utiliza:
# http://127.0.0.1:5500
#
# También permitimos:
# http://localhost:5500
#
CORS(
    app,
    resources={
        r"/*": {
            "origins": [
                "http://127.0.0.1:5500",
                "http://localhost:5500",
            ]
        }
    },
    methods=["GET", "POST", "PUT", "DELETE", "OPTIONS"],
    allow_headers=["Content-Type", "Authorization"],
)


# ============================================================
# BLUEPRINTS
# ============================================================

app.register_blueprint(users_bp)
app.register_blueprint(products_bp)
app.register_blueprint(customers_bp)
app.register_blueprint(sales_bp)


# ============================================================
# START SERVER
# ============================================================

if __name__ == "__main__":
    create_tables()
    app.run(debug=True)