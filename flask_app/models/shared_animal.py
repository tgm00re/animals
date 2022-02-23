from unittest import result
from flask_app.config.mysqlconnection import connectToMySQL

class Shared_Animal:
    def __init__(self, data):
        self.user_id = data['user_id']
        self.animal_id = data['animal_id']

    @classmethod
    def save(cls, data):
        query = "INSERT INTO shared_animals (user_id, animal_id ) VALUES (%(user_id)s, %(animal_id)s );"
        results = connectToMySQL('animals_schema').query_db(query, data)
        return results

    @classmethod 
    def has_animal(cls, data): # Takes in an animal and user id to determine if a user has already adopted an animal (true = has the animal already)
        query = "SELECT * FROM shared_animals WHERE user_id = %(user_id)s AND  animal_id = %(animal_id)s;"
        results = connectToMySQL('animals_schema').query_db(query, data)
        if len(results) < 1:
            return False
        return True # has animal already
    
    @classmethod
    def delete(cls, data):
        query = "DELETE FROM shared_animals WHERE user_id = %(user_id)s AND animal_id = %(animal_id)s;"
        return connectToMySQL('animals_schema').query_db(query, data)