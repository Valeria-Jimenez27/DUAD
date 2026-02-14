from flask import Blueprint, request, jsonify
from base_de_datos import PgManager

modification_bp = Blueprint("modification_api", __name__)

def get_db():
    return PgManager("lyfter_car_rental", "postgres", "postgres", "localhost")


# Cambiar el estado del usuario
@modification_bp.route("/users/<int:user_id>", methods=["PUT"])
def update_user_status(user_id):
    data=request.json
    db = get_db()
    query = "UPDATE users SET estado = %s WHERE id = %s"
    db.execute(query, (data["estado"], user_id))
    db.close()
    return jsonify({"User updated"})


# Cambiar el estado auto
@modification_bp.route("/cars/<int:car_id>", methods=["PUT"])
def update_car_status(car_id):
    data = request.json
    db = get_db()
    query = "UPDATE cars SET estado_automovil = %s WHERE id = %s"
    db.execute(query, (data["estado_automovil"], car_id))
    db.close()
    return jsonify({"Car updated"})


# Cambiar el estado de alquiler
@modification_bp.route("/rentals/<int:rental_id>", methods=["PUT"])
def update_rental_estado(rental_id):
    data = request.json
    db = get_db()
    query = "UPDATE rentals SET estado_alquiler = %s WHERE id = %s"
    db.execute(query, (data["estado_alquiler"], rental_id))
    db.close()
    return jsonify({"Rental updated"})
