from flask import Flask, jsonify
from users import users_bp
from cars import cars_bp
from rentals import rentals_bp


def create_app():
    app = Flask(__name__)

    @app.route("/")
    def index():
        return jsonify({"message": "API is running!"})

    app.register_blueprint(users_bp, url_prefix="/users")
    app.register_blueprint(cars_bp, url_prefix="/cars")
    app.register_blueprint(rentals_bp, url_prefix="/rentals")

    @app.errorhandler(404)
    def not_found(e):
        return jsonify({
            "error": "Not Found",
            "message": "Endpoint does not exist"
        }), 404
    return app

if __name__ == "__main__":
    app = create_app()
    app.run(debug=True, host="localhost", port=5000)

