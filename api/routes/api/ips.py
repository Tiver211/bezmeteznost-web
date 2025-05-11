from flask import Blueprint, request, jsonify
from flask_login import current_user, login_required
from mcstatus import JavaServer
from api.services.auth import verify_required
from api.services.ips import set_user_ip, clear_ips, verify_user_ip

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
    server = JavaServer("bezmetejnost.online", timeout=1)
    try:
        status = server.status()
        return jsonify({"players": status.players.online, "status": True}), 200

    except TimeoutError:
        return jsonify({"players": 0, "status": False}), 200