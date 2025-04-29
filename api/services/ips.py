from flask import request
from sqlalchemy import delete

from api.extensions import db
from api.models import UserIp, User


def set_user_ip(user_id, ip):
    ip = UserIp(user_id=user_id, ip=ip)
    db.session.add(ip)
    db.session.commit()

def clear_ips(user_id):
    stmt = delete(UserIp).where(UserIp.user_id == user_id)
    db.session.execute(stmt)
    db.session.commit()

def verify_user_ip(login, ip):
    user = User.query.filter_by(login=login).first()
    if not user:
        return False

    user_id = user.id
    ip = UserIp.query.filter_by(user_id=user_id, ip=ip).first()
    if not ip:
        return False

    return True