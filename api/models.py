from flask_login import UserMixin
from sqlalchemy.orm import relationship
import uuid
from .extensions import db, login_manager
from sqlalchemy import Integer, String, UUID, Column, ForeignKey, Boolean

class User(UserMixin, db.Model):
    __tablename__ = "users"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    mail = Column(String, nullable=False, unique=True)
    login = Column(String, nullable=False, unique=True)
    password_hash = Column(String, nullable=False)
    verify_mail = Column(Boolean, nullable=False, default=False)
    verify_admin = Column(Boolean, nullable=False, default=False)

    user_ips = relationship("UserIp", back_populates="user")
    user_alts = relationship("Alt", back_populates="user")

class UserIp(db.Model):
    __tablename__ = "users_ips"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    user_id = Column(UUID(as_uuid=True), ForeignKey("users.id"))
    ip = Column(String, nullable=False, unique=True)

    user = relationship("User", back_populates="user_ips")

class Alt(db.Model):
    __tablename__ = "alts"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    user_id = Column(UUID(as_uuid=True), ForeignKey("users.id"))
    ip = Column(String, nullable=False, unique=True)

    user = relationship("User", back_populates="user_alts")

@login_manager.user_loader
def load_user(user_id):
    return User.query.get(user_id)