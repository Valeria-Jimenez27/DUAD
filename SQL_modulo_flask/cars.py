from flask import Blueprint, request, jsonify
from base_de_datos import db

cars_bp = Blueprint("cars", __name__)


class CarRepository:

    @staticmethod
    def create(data):
        query = """
            INSERT INTO lyfter_car_rental.cars (brand, model, manufacturing_date, car_status)
            VALUES (%s, %s, %s, %s)
            RETURNING id;
        """
        params = (
            data["brand"],
            data["model"],
            data["manufacturing_date"],
            data["car_status"]
        )
        result = db.execute(query, params, fetch=True)
        return result[0]["id"]

    @staticmethod
    def update(car_id, fields):
        query = "UPDATE lyfter_car_rental.cars SET "
        values = []
        for key, value in fields.items():
            query += f"{key} = %s, "
            values.append(value)
        query = query.rstrip(", ")
        query += " WHERE id = %s;"
        values.append(car_id)
        db.execute(query, values)

    @staticmethod
    def get_by_id(car_id):
        result = db.execute(
            "SELECT * FROM lyfter_car_rental.cars WHERE id = %s;",
            (car_id,),
            fetch=True
        )
        return result[0] if result else None

    @staticmethod
    def get_all(filters):
        query = "SELECT * FROM lyfter_car_rental.cars WHERE 1=1"
        values = []
        allowed = ["id", "brand", "model", "manufacturing_date", "car_status"]
        for key, value in filters.items():
            if key in allowed:
                query += f" AND {key} = %s"
                values.append(value)
        return db.execute(query, values, fetch=True)

# Endpoints de cars
@cars_bp.route("/", methods=["POST"])
def create_car():
    try:
        data = request.get_json()
        required = ["brand", "model", "manufacturing_date", "car_status"]
        for field in required:
            if field not in data:
                return jsonify({"error": f"{field} is required"}), 400
        car_id = CarRepository.create(data)
        return jsonify({
            "message": "Car created successfully",
            "car_id": car_id
        }), 201
    except Exception as e:
        return jsonify({"error": str(e)}), 500


@cars_bp.route("/<int:car_id>", methods=["PATCH"])
def update_car(car_id):
    try:
        if not CarRepository.get_by_id(car_id):
            return jsonify({"error": "Car not found"}), 404
        data = request.get_json()
        CarRepository.update(car_id, data)
        return jsonify({"message": "Car updated successfully"}), 200
    except Exception as e:
        return jsonify({"error": str(e)}), 500


@cars_bp.route("/", methods=["GET"])
def list_cars():
    try:
        filters = request.args.to_dict()
        cars = CarRepository.get_all(filters)
        return jsonify(cars), 200
    except Exception as e:
        return jsonify({"error": str(e)}), 500
