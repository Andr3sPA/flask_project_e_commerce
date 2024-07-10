import jwt
from flask import redirect, url_for, render_template, jsonify,make_response,request
from flask_jwt_extended import jwt_required, get_jwt_identity, get_jwt
from datetime import datetime
from datetime import timedelta
from datetime import timezone
from flask_jwt_extended import (
    JWTManager, jwt_required, create_access_token, create_refresh_token,
    get_jwt_identity, set_access_cookies,
    set_refresh_cookies, unset_jwt_cookies
)
import auth
from __init__ import create_app
from flask_cors import CORS


app = create_app()


with app.app_context():
    from models import db

    db.create_all()  # Crear todas las tablas

# Using an `after_request` callback, we refresh any token that is within 30
# minutes of expiring. Change the timedeltas to match the needs of your application.
@app.after_request
def refresh_expiring_jwts(response):

    try:
        response=auth.handle_refresh_all(response)
        return response
    except (RuntimeError, KeyError):
        # Case where there is not a valid JWT. Just return the original response
        return response

@app.route("/refresh", methods=["GET"])
@jwt_required(refresh=True)
def refresh():
    return auth.handle_refresh_token()
@app.route("/required", methods=["GET"])
@jwt_required()
def required():
    return jsonify(message="This is a protected endpoint"), 200
# Only allow fresh JWTs to access this route with the `fresh=True` arguement.
@app.route('/register', methods=["POST"])
def register():
    import auth
    return auth.handleRegister()

@app.route("/login", methods=["POST"])
def login():
    import auth
    return auth.handleLogin()
@app.route("/protected", methods=["GET"])
@jwt_required()
def protected():
    return jsonify(foo="bar")
@app.route("/logout", methods=["GET"])
@jwt_required()
def logout():
    response = jsonify({"msg": "logout successful"})
    unset_jwt_cookies(response)
    return response

 
@app.route("/")
def home():
    return render_template("home.html")
@app.route("/confirm/<token>")
def confirm_email(token):
    import auth
    return auth.handle_confirm_token(token)

if __name__ == '__main__':
    app.run(debug=True)
