from flask import render_template
from flask_mail import Message
from api.extensions import mail


def send_verification_mail(token, target, login):
    msg = Message(
        subject='Verify your mail',
        recipients=[target],
        html=render_template("verif_mail.html", username=login,
                             verification_link=f"https://bezmetejnost.ru/api/auth/verify_mail?token={token}")
    )
    mail.send(msg)