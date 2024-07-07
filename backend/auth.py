# auth.py
from __future__ import print_function
from models import User
import random
import string
from pprint import pprint
import re
import sib_api_v3_sdk
from sib_api_v3_sdk.rest import ApiException
from flask import redirect, url_for, render_template, flash
from flask import request, jsonify
from flask_login import login_user
from sqlalchemy import null

from __init__ import db, bcrypt, configuration

def validar_telefono(phone_number):
    patron = r'(\+\d{1,3}[- ]?)?\d{10}|\d{3}[-]\d{3}[-]\d{4}|\(\d{3}\)\s?\d{3}[-]\d{4}|\d{3}\.\d{3}\.\d{4}'
    if re.match(patron, phone_number):
        return True
    else:
        return False

def validar_contrasena(password):
    patron = r'^(?=.*[a-z])(?=.*[A-Z])(?=.*\d)[A-Za-z\d]{8,}$'
    if re.match(patron, password):
        return True
    else:
        return False
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
    usuario = User.query.filter_by(email=email).first()
    if usuario:
        return(jsonify({'message': 'El usuario ya está registrado'}), 401)
    elif not (validar_telefono(request.form.get('phone'))):
        return(jsonify({'message': 'El telefono debe tener un formato válido'}), 401)
    elif not (validar_contrasena(request.form.get('password'))):
        return (jsonify({'message': 'La contraseña debe tener al menos 8 caracteres, contener al menos una letra mayuscula, una letra minuscula y un número.'}), 401)

    pw_hash=bcrypt.generate_password_hash(request.form.get("password_reg")).decode('utf-8')
    name=request.form.get("first_name")+" "+request.form.get("last_name")
    user = User(email=request.form.get("email_reg"),
                password=pw_hash,address=request.form.get("address"),
                name=name,city=request.form.get("city"),
                rol="user",verificationCode=generar_codigo(request.form.get("email_reg")),
                phone=request.form.get("phone"))

    confirm_url = url_for("confirm_email", token=user.verificationCode, _external=True)
    sendVerificationMail(user.email, render_template("confirm_email.html"
                                                     , confirm_url=confirm_url, Nombre=user.name))
    db.session.add(user)
    db.session.commit()
    return(jsonify({'message': 'El usuario fue registrado exitosamente'}), 200)

def handleLogin():
    user = User.query.filter_by(
    email=request.form.get("email")).first()
    if user is None:
        return (jsonify({'message': 'El usuario no existe'}), 401)
    elif user and bcrypt.check_password_hash(user.password, request.form.get("password")):
        if user.verificationCode != None:
            return (jsonify({'message': 'El email aun no ha sido confirmado'}), 401)
        login_user(user)
        return(jsonify({'message': 'Las credenciales son correctas'}), 200)
    else:
        return (jsonify({'message': 'Email o contraseña incorrectos'}), 401)


def handleLoader_user(user_id):
    return User.query.get(user_id)
def sendVerificationMail(to_email,content):
    subject="Solicitud de Confirmación de Cuenta"

    # Create an instance of the API class
    api_instance = sib_api_v3_sdk.TransactionalEmailsApi(sib_api_v3_sdk.ApiClient(configuration))
    send_smtp_email = sib_api_v3_sdk.SendSmtpEmail(
        to=[{"email": to_email}],
        sender={"email": "primaveralbordados@gmail.com"},
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
        return jsonify({"message": "La cuenta ya fue confirmada"}), 200
        return redirect(url_for("home"))

    elif verificar_codigo(token):
        usuario.verificationCode = null()
        db.session.add(usuario)
        db.session.commit()
        return jsonify({"message": "La confirmacion fue exitosa"}), 200
    else:
        return jsonify({"message": "El link de confirmación ha expirado"}), 500
    return redirect(url_for("home"))