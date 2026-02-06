import json
from flask import Flask, request, jsonify
from Data_flask import read_tasks, save_tasks


app = Flask(__name__)

#GET METHOD
@app.route("/tasks")
def get_tasks():
    tasks = read_tasks()
    estado = request.args.get("estado")
    if estado:
        tasks = [t for t in tasks if t["estado"]== estado]
    return jsonify(tasks), 200

#Codigo Reutilizable para POST y PUT
def valid_data(data, valid_id=True):
    valid_states = ["pendiente", "en progreso", "completada"]
    if not data:
        return "No hay datos"
    if valid_id and "id" not in data:
        return "El id es necesario"
    if "titulo" in data and not data["titulo"]:
        return "El título es obligatorio"
    if "descripcion" in data and not data["descripcion"]:
        return "La descripción es necesaria"
    if "estado" in data:
        if not data["estado"]:
            return "El estado es necesario"
        if data["estado"] not in valid_states:
            return "Estado inválido"
    return None

def search_tasks(tasks, id):
    for task in tasks:
        if task["id"] == id:
            return task
    return None


# POST METHOD
@app.route("/tasks", methods=["POST"])
def create_task():
    data = request.json
    tasks = read_tasks()

    error = valid_data(data)
    if error:
        return jsonify({"error": error}), 400

    if any(t["id"]==data["id"] for t in tasks):
        return jsonify({"error": "El id ya existe"}), 400

    new_task = {
        "id": data["id"],
        "titulo": data["titulo"],
        "descripcion": data["descripcion"],
        "estado": data["estado"]
    }

    tasks.append(new_task)
    save_tasks(tasks)
    return jsonify(new_task), 201


#PUT METHOD
@app.route("/tasks/<int:id>", methods=["PUT"])
def update_task(id):
    data = request.json
    tasks = read_tasks()
    error = valid_data(data, valid_id=False)
    if error:
        return jsonify({"error": error}), 400
    task = search_tasks(tasks, id)
    if not task:
        return jsonify({"error": "Tarea no encontrada"}), 404

    task["titulo"] = data.get("titulo", task["titulo"])
    task["descripcion"] = data.get("descripcion", task["descripcion"])
    task["estado"] = data.get("estado", task["estado"])

    save_tasks(tasks)
    return jsonify(task), 200


#DELETE METHOD
@app.route("/tasks/<int:id>", methods=["DELETE"])
def delete_task(id):
    tasks = read_tasks()
    task = search_tasks(tasks, id)
    if not task:
        return jsonify({"error": "Tarea no encontrada"}), 404
    tasks.remove(task)
    save_tasks(tasks)
    return jsonify({"mensaje": "Tarea eliminada correctamente"}), 200


if __name__ == "__main__":
    app.run(debug=True)
