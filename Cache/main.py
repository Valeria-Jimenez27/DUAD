from dotenv import load_dotenv
load_dotenv()

from flask import Flask
from endpoints import api
from engine import create_tables

app = Flask(__name__)
app.register_blueprint(api)

if __name__ == "__main__":
    create_tables()
    app.run(debug=True)