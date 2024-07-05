# auth.py
from __future__ import print_function
from models import User
import random
import string
from datetime import datetime
from pprint import pprint

import sib_api_v3_sdk
from sib_api_v3_sdk.rest import ApiException
from flask import redirect, url_for, render_template, flash
from flask import request, jsonify
from flask_login import UserMixin, current_user
from flask_login import login_user
from sqlalchemy import null

from __init__ import db, bcrypt, configuration

def generar_codigo(email):
    caracteres = string.ascii_letters + string.digits
    codigo_aleatorio = ''.join(random.choice(caracteres) for _ in range(12))
    codigo_completo = f"{email}:{codigo_aleatorio}"
    return codigo_completo

def extraer_datos(codigo_completo):
    email, codigo_aleatorio = codigo_completo.split(':')
    return email
def verificar_codigo(codigo):
    email= extraer_datos(codigo)
    usuario = User.query.filter_by(verificationCode=codigo).first()

    if usuario.email==email :
        usuario.verificationCode=null()
        return True
def handleRegister():
    email = request.form.get('email')
    if request.method == "POST":
        usuario = User.query.filter_by(email=email).first()
        if usuario:
            return jsonify({"mensaje": "El email ya está registrado"})
        pw_hash=bcrypt.generate_password_hash(request.form.get("password")).decode('utf-8')
        user = User(email=request.form.get("email"),
                    password=pw_hash,address=request.form.get("address"),
                    nameRestaurant=request.form.get("nameRestaurant"),
                    rol="user",verificationCode=generar_codigo(request.form.get("email")))

        confirm_url = url_for("confirm_email", token=user.verificationCode, _external=True)
        sendVerificationMail(user.email,render_template("confirm_email.html"
                                                               ,confirm_url=confirm_url,Nombre=user.nameRestaurant))
        db.session.add(user)
        db.session.commit()
        return redirect(url_for("login"))
    return render_template("sign_up.html")

def handleLogin():
    if request.method == "POST":

        user = User.query.filter_by(
            email=request.form.get("email")).first()

        if user is None:
            return jsonify({"mensaje": "El usuario no existe"})
        elif user and bcrypt.check_password_hash(user.password, request.form.get("password")):
            if user.verificationCode != None:
                return jsonify({"mensaje": "El email aun no ha sido confirmado"})
            login_user(user)
            return redirect(url_for("home"))
        else:
            return jsonify({"mensaje": "Email o contraseña incorrectos"})
    return render_template("login.html")

def handleLoader_user(user_id):
    return User.query.get(user_id)
def sendVerificationMail(to_email,content):
    subject="Solicitud de Confirmación de Cuenta"

    # Create an instance of the API class
    api_instance = sib_api_v3_sdk.TransactionalEmailsApi(sib_api_v3_sdk.ApiClient(configuration))
    send_smtp_email = sib_api_v3_sdk.SendSmtpEmail(
        to=[{"email": to_email}],
        sender={"email": "duquepatatas@gmail.com"},
        subject=subject,
        html_content=content
    )

    try:
        # Send a transactional email
        api_response = api_instance.send_transac_email(send_smtp_email)
        pprint(api_response)
        return jsonify({"message": "Email sent successfully!"}), 200
    except ApiException as e:
        print("Exception when calling TransactionalEmailsApi->send_transac_email: %s\n" % e)
        return jsonify({"error": "Failed to send email"}), 500

def handle_confirm_token(token):
    email=extraer_datos(token)
    usuario = User.query.filter_by(email=email).first()

    if usuario.verificationCode == None:
        flash("Account already confirmed.", "success")
        return redirect(url_for("home"))

    elif verificar_codigo(token):
        usuario.verificationCode = null()
        db.session.add(usuario)
        db.session.commit()
        flash("You have confirmed your account. Thanks!", "success")
    else:
        flash("The confirmation link is invalid or has expired.", "danger")
    return redirect(url_for("home"))