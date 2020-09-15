from flask import render_template, flash, redirect, url_for, make_response

from flask_web import db
from flask_web.main import bp
from flask_web.main.forms import Login
from flask_web.models import User
from flask_login import current_user, login_user, logout_user, login_required


@bp.route("/", methods=["GET"])
@bp.route("/index", methods=["GET"])
@login_required
def index():
    user = {"firstName": current_user.first_name, "lastName": current_user.last_name}
    return render_template("index.html", title='Dashboard', user=user)


@bp.route('/logout')
def logout():
    logout_user()
    return redirect(url_for('main.index'))


@bp.route('/login', methods=['GET', 'POST'])
def login():
    if current_user.is_authenticated:
        return redirect(url_for('main.index'))
    form = Login()
    if form.validate_on_submit():
        user = User.query.filter_by(email=form.email.data.lower()).first()
        if user is None or not user.check_password(form.password.data):
            flash('Invalid username or password')
            return redirect(url_for('main.login'))
        login_user(user, remember=form.remember_me.data)
        return redirect(url_for('main.index'))
    return render_template('login.html', title='Sign In', form=form)


@bp.route('/api/v1/test', methods=["GET"])
def test_endpoint():
    response_json = {"test": "yep"}
    response = make_response(response_json, 200)
    response.headers["Content-Type"] = "application/json"
    return response
