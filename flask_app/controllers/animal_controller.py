from flask_app import app
from flask_app.models import animal, user, shared_animal
from flask import request, render_template, redirect, session
from flask import flash

@app.route('/create_animal')
def create_animal():
    if 'user_id' not in session:
        return redirect('/')
    return render_template("add_animal.html")

@app.route('/create_animal_form', methods=['POST'])
def create_animal_form():
    if not animal.Animal.validate_animal(request.form):
        return redirect('/create_animal')
    data = {
        "name": request.form['name'],
        "type": request.form['type']
    }
    animal_id = animal.Animal.save(data)
    shared_data = {
        "user_id": session['user_id'],
        "animal_id": animal_id
    }
    shared_animal.Shared_Animal.save(shared_data)
    return redirect('/dashboard')
    
@app.route('/view_animals')
def view_animals():
    if "user_id" not in session:
        return redirect('/')
    animals = animal.Animal.get_all()
    return render_template("view_animals.html", animals=animals)

@app.route('/adopt_animal/<int:animal_id>')
def adopt_animal(animal_id):
    if 'user_id' not in session:
        return redirect('/')
    data = {
        "animal_id": animal_id,
        "user_id": session['user_id']
    }
    if shared_animal.Shared_Animal.has_animal(data): # user already has animal
        flash("You have already adopted this animal!", "adoption")
    else:
        flash("You just adopted a new animal!", "adoption")
        shared_animal.Shared_Animal.save(data)
    return redirect('/view_animals')    


@app.route('/edit_animal/<int:animal_id>')
def edit_animal(animal_id):
    data = {
        "user_id": session['user_id'],
        "animal_id": animal_id
    }
    if not shared_animal.Shared_Animal.has_animal(data):
        return redirect('/dashboard')
    the_animal = animal.Animal.get_by_id(data)
    return render_template("edit_animal.html", animal=the_animal)

@app.route('/edit_animal_form/<int:id>', methods=['POST'])
def edit_animal_form(id):
    print("Updating animal!")
    print(id)
    data = {
        "id": id,
        "name": request.form['name'],
        "type": request.form['type']
    }
    animal.Animal.update(data)
    return redirect('/dashboard')


@app.route('/view_animal/<int:id>')
def view_animal(id):
    if 'user_id' not in session:
        return redirect('/')
    data = {
        "id": id
    }
    the_animal = animal.Animal.get_animal_with_users(data)
    return render_template("view_animal.html", animal=the_animal)