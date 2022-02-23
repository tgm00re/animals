from flask import render_template, request, redirect, session, flash
from flask_app import app
from flask_app.models import shared_animal

@app.route('/delete_connection/<int:user_id>/<int:animal_id>')
def delete_connection(user_id, animal_id):
    if user_id != session['user_id']:
        return redirect('/logout')
    data = { 
        "user_id": user_id,
        "animal_id": animal_id
    }
    shared_animal.Shared_Animal.delete(data)
    return redirect('/dashboard')