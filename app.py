from flask import redirect, url_for, render_template
from flask_login import logout_user, login_required
from flask_validators import validate_form
from __init__ import create_app

app = create_app()
with app.app_context():
    from models import db
    db.create_all()  # Crear todas las tablas
@validate_form('email', 'password','address','nameRestaurant')
@app.route('/register', methods=["GET", "POST"])
def register():
    import auth
    return auth.handleRegister()
@app.login_manager.unauthorized_handler
def unauthorized_handler():
    return 'Unauthorized', 401
@app.route("/login", methods=["GET", "POST"])
def login():
    import auth
    return auth.handleLogin()

@app.route("/logout")
def logout():
    logout_user()
    return redirect(url_for("home"))

@app.route("/")
def home():
    return render_template("home.html")
@app.route('/send_email')
def send_email():
    import auth
    auth.sendVerificationMail()
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
