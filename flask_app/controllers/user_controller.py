from unicodedata import name
from flask import render_template, request, redirect, session, flash
from flask_app import app
from flask_app.models import user
from flask_bcrypt import Bcrypt

bcrypt = Bcrypt(app)


@app.route('/')
def index():
    if 'user_id' in session:
        return redirect('/dashboard')
    return render_template("index.html")

@app.route('/register', methods=['POST'])
def register():
    if not user.User.validate_user(request.form):
        return redirect('/')
    
    pw_hash = bcrypt.generate_password_hash(request.form['password'])
    data = {
        "name": request.form['name'],
        "email": request.form['email'],
        "password": pw_hash
    }
    if user.User.get_by_email(data):
        flash("Email already exists", 'register')
        return redirect('/')
    new_id = user.User.save(data)
    print("PRINTING NEW ID")
    print(new_id)
    session['user_id'] = new_id
    session['user_first'] = data['name']
    return redirect('/dashboard')

@app.route('/login', methods=['POST'])
def login():
    user_in_db = user.User.get_by_email({ "email": request.form['email']})
    if not user_in_db:
        flash("Incorrect email/password", 'login')
        return redirect('/')
    if not bcrypt.check_password_hash(user_in_db.password, request.form['password']):
        flash("Incorrect email/password", 'login')
        return redirect('/')
    session['user_id'] = user_in_db.id
    session['user_name'] = user_in_db.name
    return redirect('/')

@app.route('/dashboard')
def dashboard():
    if 'user_id' not in session:
        return redirect('/')
    print(session['user_id'])
    data = {
        "id": session['user_id']
    }
    user_with_animals = user.User.get_user_with_animals(data)
    return render_template("dashboard.html", user=user_with_animals)

@app.route('/view_user/<int:user_id>')
def view_user(user_id):
    if 'user_id' not in session:
        return redirect('/')
    data = {
        "id": user_id
    }
    the_user = user.User.get_user_with_animals(data)
    return render_template("view_user.html", user=the_user)
    


@app.route('/logout')
def logout():
    session.clear()
    return redirect('/')