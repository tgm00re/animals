from flask_app import app
from flask_app.controllers import user_controller, animal_controller, shared_animal_controller

if __name__ == "__main__":
    app.run(debug=True)