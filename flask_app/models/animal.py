from tkinter.tix import Select
from flask_app.config.mysqlconnection import connectToMySQL
from flask_app.models import user
from flask import flash

class Animal:
    def __init__(self, data):
        self.id = data['id']
        self.name = data['name']
        self.type = data['type']
        self.created_at = data['created_at']
        self.updated_at = data['updated_at']
        self.users = []

    @classmethod
    def save(cls, data):
        query = "INSERT INTO animals (name, type, created_at, updated_at ) VALUES (%(name)s, %(type)s, NOW(), NOW() );"
        results = connectToMySQL('animals_schema').query_db(query, data)
        return results

    @classmethod
    def get_animal_with_users(cls, data):
        query = "SELECT * FROM animals LEFT JOIN shared_animals ON animals.id = shared_animals.animal_id LEFT JOIN users ON shared_animals.user_id = users.id WHERE animals.id = %(id)s;"
        results = connectToMySQL('animals_schema').query_db(query,data)
        animal = cls( results[0] )

        for row_from_db in results:
            #Created instances of users
            user_data = {
                "id": row_from_db['users.id'],
                "name": row_from_db['users.name'],
                "email": row_from_db['email'],
                "password": row_from_db['password'],
                "created_at": row_from_db['users.created_at'],
                "updated_at": row_from_db['users.updated_at'],
            }
            animal.users.append( user.User(user_data) )
        #Recall, we are returning one animal with a list of users
        return animal

    @classmethod
    def get_all(cls):
        query = "SELECT * FROM animals"
        results = connectToMySQL('animals_schema').query_db(query)
        animals = []
        for result in  results:
            animals.append( cls(result) )
        return animals
    
    @classmethod
    def get_by_id(cls, data):
        query = "SELECT * FROM animals WHERE id = %(animal_id)s;"
        result = connectToMySQL('animals_schema').query_db(query, data)
        return cls( result[0] )

    @classmethod
    def update(cls, data):
        query = "UPDATE animals SET name=%(name)s, type=%(type)s, updated_at=NOW() WHERE id = %(id)s;"
        return connectToMySQL('animals_schema').query_db(query, data)

    @staticmethod
    def validate_animal(animal):
        is_valid = True
        if len(animal['name']) < 2:
            flash("Name must be 2 or more characters", 'create')
            is_valid = False
        return is_valid