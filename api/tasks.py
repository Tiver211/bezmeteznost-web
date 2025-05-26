from .extensions import socketio, redis_client
from mcstatus import JavaServer
from datetime import datetime
import logging
logger = logging.getLogger(__name__)

def check_minecraft_server():
    server = JavaServer("bezmetejnost.online", timeout=1)

    try:
        status = server.status()
        online = True
        players = status.players.online
    except (TimeoutError, ConnectionRefusedError):
        online = False
        players = 0

    old_players = redis_client.get("players")
    old_online = redis_client.get("online")
    if old_online is None:
        old_online = False
    else:
        old_online = bool(int(old_online))

    if old_players is None:
        old_players = False
    else:
        old_players = int(old_players)
    if old_players != players or old_online != online:
        update_server_status(online, players)


def update_server_status(online, players):
    # Сохраняем в Redis
    redis_client.set("players", players)
    redis_client.set("online", int(online))

    # Отправляем обновление через Socket.IO
    server_status = {
        'online': online,
        'players': players,
    }
    socketio.emit('status_update', server_status)
