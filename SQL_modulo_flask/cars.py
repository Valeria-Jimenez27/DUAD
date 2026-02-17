from flask import Blueprint, request, jsonify
from base_de_datos import PgManager


db = PgManager(
    db_name="lyfter_car_rental",
    user="postgres",
    password="postgres",
    host="localhost"
)

cars_bp = Blueprint("cars", __name__)

# Repositorio de cars
class CarRepository:
    @staticmethod
    def create_car(car_data):
        query = """
            INSERT INTO lyfter_car_rental.cars (marca, modelo, fecha_fabricacion, estado_automovil)
            VALUES (%s, %s, %s, %s)
            RETURNING id;
        """
        params = (
            car_data["marca"],
            car_data["modelo"],
            car_data["fecha_fabricacion"],
            car_data["estado_automovil"]
        )
        result = db.execute(query, params, fetch=True)
        return result[0]["id"] if result else None


    @staticmethod
    def update_estado_automovil(car_id, estado_automovil):
        query = """
            UPDATE lyfter_car_rental.cars
            SET estado_automovil = %s
            WHERE id = %s;
        """
        db.execute(query, (estado_automovil, car_id))


    @staticmethod
    def get_all(filters):
        query = "SELECT * FROM lyfter_car_rental.cars WHERE 1=1"
        values = []
        allowed_filters = [
            "id", "marca", "modelo",
            "fecha_fabricacion", "estado_automovil"
        ]
        for key, value in filters.items():
            if key in allowed_filters:
                query += f" AND {key} = %s"
                values.append(value)
        return db.execute(query, values, fetch=True)


#ENDPOINTS DE CARS
@cars_bp.route("/", methods=["POST"])
def create_automovil():
    try:
        data = request.get_json()
        if not data:
            return jsonify({"error": "Request body is required"}), 400
        required_fields = [
            "marca",
            "modelo",
            "fecha_fabricacion",
            "estado_automovil"
        ]
        for field in required_fields:
            if field not in data or not data[field]:
                return jsonify({"error": f"{field} is required"}), 400
        car_id = CarRepository.create_car(data)
        return jsonify({
            "message": "Car created successfully",
            "car_id": car_id
        }), 201
    except Exception as e:
        return jsonify({
            "error": "Error creating car",
            "details": str(e)
        }), 500

@cars_bp.route("/<int:car_id>/estado_automovil", methods=["PATCH"])
def update_car_estado_automovil(car_id):
    try:
        data = request.get_json()
        if not data or "estado_automovil" not in data:
            return jsonify({"error": "estado_automovil is required"}), 400
        CarRepository.update_estado_automovil(car_id, data["estado_automovil"])
        return jsonify({
            "message": "Car estado_automovil updated successfully"
        }), 200
    except Exception as e:
        return jsonify({
            "error": "Error updating car estado_automovil",
            "details": str(e)
        }), 500

@cars_bp.route("/", methods=["GET"])
def list_cars():
    try:
        filters = request.args.to_dict()
        cars = CarRepository.get_all(filters)
        return jsonify(cars), 200
    except Exception as e:
        return jsonify({
            "error": "Error listing cars",
            "details": str(e)
        }), 500
