from flask_app.config.mysqlconnection import connectToMySQL
from flask import flash
import re
from flask_app.models import animal

EMAIL_REGEX = re.compile(r'^[a-zA-Z0-9.+_-]+@[a-zA-Z0-9._-]+\.[a-zA-Z]+$') 


class User:
    def __init__(self, data):
        self.id = data['id']
        self.name = data['name']
        self.email = data['email']
        self.password = data['password']
        self.created_at = data['created_at']
        self.updated_at = data['updated_at']
        self.animals = []

    @classmethod
    def save(cls, data):
        query = "INSERT INTO users (name, email, password, created_at, updated_at ) VALUES (%(name)s, %(email)s, %(password)s, NOW(), NOW() )"
        results = connectToMySQL('animals_schema').query_db(query, data)
        return results

    @classmethod
    def get_by_email(cls, data):
        query = "SELECT * FROM users WHERE email = %(email)s"
        result = connectToMySQL('animals_schema').query_db(query, data)
        if len(result) < 1:
            return False #nobody with email
        return cls(result[0])

    @classmethod
    def get_user_with_animals(cls, data):
        query = "SELECT * FROM users LEFT JOIN shared_animals ON users.id = shared_animals.user_id LEFT JOIN animals ON shared_animals.animal_id = animals.id WHERE users.id = %(id)s;"
        results = connectToMySQL('animals_schema').query_db(query, data)
        user = cls( results[0] )
        
        for row_from_db in results:
            #Create instances of animals
            animal_data = {
                "id": row_from_db["animals.id"],
                "name": row_from_db["animals.name"],
                "type": row_from_db["type"],
                "created_at": row_from_db["created_at"],
                "updated_at": row_from_db["updated_at"]
            }
            user.animals.append( animal.Animal(animal_data) )
        #Recall, a single user is being returned with a list of animals.
        return user

    @staticmethod
    def validate_user(user):
        is_valid = True
        if len(user['name']) < 2:
            flash("Name must be 2 or more characters", 'register')
            is_valid = False
        if not EMAIL_REGEX.match(user['email']):
            flash("Invalid email address", 'register')
            is_valid = False
        if len(user['password']) < 3:
            flash("Password must be 3 or more characters", 'register')
            is_valid = False
        if user['password'] != user['confirm_password']:
            flash("Passwords didn't match.")
            is_valid = False
        return is_valid
        

    