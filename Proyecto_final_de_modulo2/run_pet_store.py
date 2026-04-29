from dotenv import load_dotenv
load_dotenv()

from flask import Flask
from app.routes.users import users_bp
from app.routes.products import products_bp
from app.routes.customers import customers_bp
from app.routes.sales import sales_bp
from app.database.engine import create_tables
from app.services.Cache import cache_manager



app = Flask(__name__)
app.register_blueprint(users_bp)
app.register_blueprint(products_bp)
app.register_blueprint(customers_bp)
app.register_blueprint(sales_bp)

if __name__ == "__main__":
    create_tables()
    app.run(debug=True)