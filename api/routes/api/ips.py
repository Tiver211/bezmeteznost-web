from flask import Blueprint, request, jsonify
from flask_login import current_user, login_required
from mcstatus import JavaServer
from api.services.auth import verify_required
from api.services.ips import set_user_ip, clear_ips, verify_user_ip
from api.extensions import redis_client

blueprint = Blueprint("ips", __name__, url_prefix="/ips")

@blueprint.route("/set", methods=["POST"])
@login_required
@verify_required
def set_ip():
    code, msg = set_user_ip(current_user.id, request.headers.get("X-Real-IP"))
    return jsonify({"msg": msg}), code

@blueprint.route("/clear", methods=["POST"])
@login_required
@verify_required
def clear_ip():
    clear_ips(current_user.id)
    return jsonify({"msg": "ok"}), 200

@blueprint.route("/verify", methods=["POST"])
def verify_ip():
    user_ip = request.json.get("user_ip")
    login = request.json.get("login")

    res = verify_user_ip(login, user_ip)
    if res:
        return jsonify({"msg": "ok"}), 200

    return jsonify({"msg": "incorrect ip"}), 404

@blueprint.route("/server_status", methods=["GET"])
def server_status():
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
    return jsonify({"players": players, "status": online}), 200

