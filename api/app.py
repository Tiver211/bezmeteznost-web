import os
from api.routes import blueprint
from flask import Flask, jsonify
from extensions import *

app = Flask(__name__)

app.config["JWT_SECRET_KEY"] = os.getenv('RANDOM_SECRET')
app.config["SQLALCHEMY_DATABASE_URI"] = os.getenv("POSTGRES_CONN")

jwt.init_app(app)
db.init_app(app)

app.register_blueprint(blueprint)

@app.route('/api/ping')
def ping():
    return jsonify({"status": "ok"}), 200

if __name__ == "__main__":
    app.run(debug=True, host="0.0.0.0", port=80)
