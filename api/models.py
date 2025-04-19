from sqlalchemy.orm import relationship

from extensions import db
from sqlalchemy import Integer, String, UUID, Column, ForeignKey


class User(db.Model):
    __tablename__ = "users"

    id = Column(UUID(as_uuid=True), primary_key=True)
    login = Column(String, nullable=False, unique=True)
    password_hash = Column(String, nullable=False)

    user_ips = relationship("UserIp", back_populates="user")

class UserIp(db.Model):
    __tablename__ = "users_ips"

    id = Column(UUID(as_uuid=True), primary_key=True)
    user_id = Column(UUID(as_uuid=True), ForeignKey("users.id"))

    user = relationship("User", back_populates="user_ips")
