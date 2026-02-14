from flask import Flask
from creation_api import creation_bp
from modification_api import modification_bp
from listing_api import listing_bp

app = Flask(__name__)

@app.route("/")
def home():
    return {"message": "API connected successfully"}

app.register_blueprint(creation_bp)
app.register_blueprint(modification_bp)
app.register_blueprint(listing_bp)

if __name__ == "__main__":
    app.run(debug=True)
