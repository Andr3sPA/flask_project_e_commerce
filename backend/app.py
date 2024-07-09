import jwt
from flask import redirect, url_for, render_template, jsonify
from flask_jwt_extended import jwt_required, get_jwt_identity, get_jwt
import redis
from __init__ import create_app, ACCESS_EXPIRES
from flask_cors import CORS
app = create_app()
CORS(app)


with app.app_context():
    from models import db, User

    db.create_all()  # Crear todas las tablas


@app.route('/register', methods=["POST"])
def register():
    import auth
    return auth.handleRegister()
@app.login_manager.unauthorized_handler
def unauthorized_handler():
    return 'Unauthorized', 401
@app.route("/login", methods=["POST"])
def login():
    import auth
    return auth.handleLogin()
@app.route("/protected", methods=["GET"])
@jwt_required()
def protected():
    # Access the identity of the current user with get_jwt_identity
    current_user = get_jwt_identity()
    return jsonify(logged_in_as=current_user), 200

 
@app.route("/")
def home():
    return render_template("home.html")
@app.route("/confirm/<token>")
def confirm_email(token):
    import auth
    return auth.handle_confirm_token(token)
@app.login_manager.user_loader
def loader_user(user_id):
    import auth
    return auth.handleLoader_user(user_id)
if __name__ == '__main__':
    app.run(debug=True)
