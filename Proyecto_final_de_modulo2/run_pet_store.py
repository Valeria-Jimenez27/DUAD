from dotenv import load_dotenv
load_dotenv()

from flask import Flask
from users import users_bp
from products import products_bp
from sales import sales_bp
from engine import create_tables
from Cache import cache_manager
from customers import customers_bp


app = Flask(__name__)
app.register_blueprint(users_bp)
app.register_blueprint(products_bp)
app.register_blueprint(customers_bp)
app.register_blueprint(sales_bp)

if __name__ == "__main__":
    create_tables()
    app.run(debug=True)