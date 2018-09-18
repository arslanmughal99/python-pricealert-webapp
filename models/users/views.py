from flask import Blueprint, request, session, redirect, url_for, render_template
from models.users.decorator import requires_login
from models.users.user import User
from models.users import errors as UserErrors




user_blueprint = Blueprint('user',__name__)

@user_blueprint.route('/login', methods = ['GET','POST'])
def login_user():
    if request.method == 'POST':
        email = request.form['email']
        password = request.form['password']
        try:
            if User.is_login_valid(email, password):
                session['email'] = email
                return redirect(url_for(".user_alerts"))

        except UserErrors.UserErrors as e:
            return e.message
    return render_template("user/login.html")




@user_blueprint.route('/register', methods=['GET','POST'])
def register_user():
    if request.method == 'POST':
        email = request.form['email']
        password = request.form['password']
        try:
            if User.register_user(email, password):
                session['email'] = email
                return redirect(url_for(".user_alerts"))
        except UserErrors.UserErrors as e:
            return e.message
    return render_template('user/register.html')


@user_blueprint.route('/alerts')
@requires_login
def user_alerts():
    user = User.find_by_email(session["email"])
    alert = user.get_alerts()
    return  render_template("user/alerts.html", alerts=alert)


@user_blueprint.route('/logout')
def logout_user():
    session['email'] = None
    return redirect(url_for('home'))


@user_blueprint.route('check_alert/<string:user_id>')
def check_user_alerts(user_id):
    pass
