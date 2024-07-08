import jwt
from flask import redirect, url_for, render_template, jsonify
from flask_jwt_extended import jwt_required, get_jwt_identity, get_jwt
from flask_jwt_extended.jwt_manager import JWTManager
from flask_login import logout_user, login_required, current_user
import redis
from __init__ import create_app, ACCESS_EXPIRES
from flask_cors import CORS
app = create_app()
CORS(app)
jwt_redis_blocklist = redis.StrictRedis(
    host="localhost", port=6379, db=0, decode_responses=True
)

with app.app_context():
    from models import db, User

    db.create_all()  # Crear todas las tablas
# Callback function to check if a JWT exists in the redis blocklist
@jwt.token_in_blocklist_loader
def check_if_token_is_revoked(jwt_header, jwt_payload: dict):
    jti = jwt_payload["jti"]
    token_in_redis = jwt_redis_blocklist.get(jti)
    return token_in_redis is not None
# Register a callback function that loads a user from your database whenever
# a protected route is accessed. This should return any python object on a
# successful lookup, or None if the lookup failed for any reason (for example
# if the user has been deleted from the database).
@jwt.user_lookup_loader
def user_lookup_callback(_jwt_header, jwt_data):
    identity = jwt_data["sub"]
    return User.query.filter_by(id=identity).one_or_none()
@app.route("/logout", methods=["DELETE"])
@jwt_required()
def logout():
    jti = get_jwt()["jti"]
    jwt_redis_blocklist.set(jti, "", ex=ACCESS_EXPIRES)
    return jsonify(msg="Access token revoked")
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
