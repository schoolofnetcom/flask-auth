import os
from flask import Flask, request, url_for, redirect, render_template, jsonify
from flask_login import login_user, logout_user, login_required
from models.User import User
from config import login_manager, app, db

@login_manager.user_loader
def load_user(id):
    return User.query.get(int(id))

@app.route('/')
@login_required
def hello():
    return render_template('hello.html')

@login_manager.request_loader
def load_from_request(request):
    key = request.headers.get('Authorization')

    if key:
        key = key.replace('Basic ', '', 1)
        try:
            key = base64.b64decode(key)
            key = key.split(key)[0]
        except TypeError:
            pass

        user = User.query.filter_by(username = key).first()

        if user:
            return user

    return None


@app.route('/users/register', methods = ['GET', 'POST'])
def register():
    if request.method == 'GET':
        return render_template('register.html')

    user = User(request.form['username'], request.form['password'], request.form['email'])
    db.session.add(user)
    db.session.commit()

    return redirect(url_for('login'))

@app.route('/login', methods = ['GET', 'POST'])
def login():
    if request.method == 'GET':
        return render_template('login.html')

    user = User.query.filter_by(username = request.form['username']).first()

    if user is None:
        return redirect(url_for('login'))
    if not user.check_password(request.form['password']):
        return redirect(url_for('login'))

    remember = False

    if 'remember_me' in request.form:
        remember = True

    login_user(user, remember = remember)

    return redirect(url_for('hello'))

@app.route('/login/key', methods = ['GET', 'POST'])
def loginKey():
    if request.method == 'GET':
        return render_template('login.html')

    user = User.query.filter_by(username = request.form['username']).first()

    if user is None:
        return redirect(url_for('login'))
    if not user.check_password(request.form['password']):
        return redirect(url_for('login'))

    remember = False

    if 'remember_me' in request.form:
        remember = True

    login_user(user, remember = remember)

    return jsonify(key = request.headers.get('Authorization'))

@app.route('/logout', methods = ['GET'])
@login_required
def logout():
    logout_user()
    return redirect(url_for('login'))

@login_manager.unauthorized_handler
def unauthorized_cb():
    return render_template('401.html')
    # return redirect('login')


if __name__ == '__main__':
    app.run(debug = True)