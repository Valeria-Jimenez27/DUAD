from flask import Flask
from engine import create_tables
from endpoints import api

app = Flask(__name__)

create_tables()

app.register_blueprint(api)

if __name__ == "__main__":
    app.run(debug=True)