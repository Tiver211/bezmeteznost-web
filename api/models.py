from flask_login import UserMixin
from sqlalchemy.orm import relationship
import uuid
from .extensions import db, login_manager
from sqlalchemy import Integer, String, UUID, Column, ForeignKey


class User(UserMixin, db.Model):
    __tablename__ = "users"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    login = Column(String, nullable=False, unique=True)
    password_hash = Column(String, nullable=False)

    user_ips = relationship("UserIp", back_populates="user")

class UserIp(db.Model):
    __tablename__ = "users_ips"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    user_id = Column(UUID(as_uuid=True), ForeignKey("users.id"))
    ip = Column(String, nullable=False)

    user = relationship("User", back_populates="user_ips")

@login_manager.user_loader
def load_user(user_id):
    return User.query.get(user_id)