import os
from api.routes import blueprint
from flask import Flask, jsonify, redirect, url_for, request
from .extensions import *
from .models import *

app = Flask(__name__)

app.config["SECRET_KEY"] = os.getenv('RANDOM_SECRET')
app.config["SQLALCHEMY_DATABASE_URI"] = os.getenv("POSTGRES_CONN")
app.config['MAIL_SERVER'] = 'postbox.cloud.yandex.net'
app.config['MAIL_PORT'] = 587
app.config['MAIL_USE_TLS'] = True
app.config['MAIL_USE_SSL'] = False
app.config['MAIL_USERNAME'] = 'API_KEY'
app.config['MAIL_PASSWORD'] = os.getenv("SMTP_PASS")
app.config['MAIL_DEFAULT_SENDER'] = 'noreply@bezmetejnost.ru'

login_manager.init_app(app)
db.init_app(app)
mail.init_app(app)

login_manager.login_view = 'main.pages.login_page'
app.register_blueprint(blueprint)

with app.app_context():
    db.create_all()

@app.route('/api/ping')
def ping():
    return jsonify({"status": "ok"}), 200

if __name__ == "__main__":
    app.run(debug=True, host="0.0.0.0", port=80)
