from gevent import monkey
monkey.patch_all()

import os
from flask_socketio import emit

from api.routes import blueprint
from flask import Flask, jsonify, redirect, url_for, request
from .extensions import *
from .models import *
from .tasks import check_minecraft_server
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
app.config["JOBS"] = [
    {
        "id": "check_minecraft_server",  # Уникальный ID задачи
        "func": check_minecraft_server,         # Функция для выполнения
        "trigger": "interval",       # Тип триггера (интервал)
        "seconds": 5               # Интервал в секундах
    }
]

login_manager.init_app(app)
db.init_app(app)
mail.init_app(app)
migrate.init_app(app)
socketio.init_app(app)
scheduler.init_app(app)
scheduler.start()

login_manager.login_view = 'main.pages.login_page'
app.register_blueprint(blueprint)

with app.app_context():
    db.create_all()

@socketio.on("connect")
def on_connect():
    players = redis_client.get("players")
    online = redis_client.get("online")
    if online is None:
        online = False
    else:
        online = bool(int(online))

    if players is None:
        players = 0
    else:
        players = int(players)

    status = {'online': online, 'players': players}
    emit('status_update', status)

@app.route('/api/ping')
def ping():
    return jsonify({"status": "ok"}), 200

if __name__ == "__main__":
    app.run(debug=True, host="0.0.0.0", port=80)
