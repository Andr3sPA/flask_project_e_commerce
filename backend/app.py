from flask import redirect, url_for, render_template
from flask_login import logout_user, login_required
from __init__ import create_app
from flask_cors import CORS
app = create_app()
CORS(app)
with app.app_context():
    from models import db
    db.create_all()  # Crear todas las tablas

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
@app.route('/data')
def get_data():
    # Returning an api for showing in reactjs
    return {
        'Name': "geek",
        "Age": "22",
        "programming": "python"
    }
 
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
