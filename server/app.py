#!/usr/bin/env python3

# Standard library imports
import os

# Remote library imports
from flask import session, request, send_from_directory
from flask_restful import Resource
from werkzeug.utils import secure_filename

# Local imports
from config import app, db, api

# Model imports
from models import User, Pet, MedicationLog

# Check if images exist
os.makedirs(app.config['IMAGES_FOLDER'], exist_ok=True)

# Allow image extensions
ALLOWED_EXTENSIONS = {'png', 'jpg', 'jpeg', 'gif'}
def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

# Views go here!
@app.route('/')
def index():
    return '<h1>Welcome to the Project Server!</h1>'

# Authorization
def authorize():
    user_id = session.get('user_id')
    if not user_id:
        return None
    return User.query.get(user_id)

@app.before_request
def check_if_logged_in():
    public_endpoints = ['index', 'signup', 'login', 'checksession']
    if request.endpoint in public_endpoints:
        return
    if not session.get('user_id'):
        return {"error" : "Unauthorized"}, 401

# Authorization endpoints
class Signup(Resource):
    def post(self):
        data = request.get_json()

        errors = []

        # Conditions
        if not data.get('username'):
            errors.append("Username is required")
        if not data.get('password'):
            errors.append("Password is required")
        if not data.get('name'):
            errors.append("Name is required")
        if not data.get('email'):
            errors.append("Email is required")
        if not data.get('role'):
            errors.append("Role is required")
        if User.query.filter(db.func.lower(User.username) == data['username'].lower()).first():
            errors.append("Username already exists")
        if User.query.filter(db.func.lower(User.email) == data['email'].lower()).first():
            errors.append("Email already exists")
        if errors:
            return {"errors": errors}, 422

        user = User (
            username=data['username'],
            name=data['name'],
            email=data['email'],
            role=data['role']
        )
        user.password_hash = data['password']

        db.session.add(user)
        db.session.commit()

        session['user_id'] = user.id

        return user.to_dict(), 201

class CheckSession(Resource):
    def get(self):
        user_id = session.get('user_id')

        if user_id:
            user = db.session.get(User, user_id)
            if user:
                return {
                    "id": user.id,
                    "username": user.username,
                    "role": user.role
                }, 200
        return {"error": "Unauthorized"}, 401

class Login(Resource):
    def post(self):
        data = request.get_json()

        username = data.get('username')
        password = data.get('password')

        if not username:
            return {"error": "Username is required"}, 400
        if not password:
            return {"error": "Password is required"}, 400

        user = User.query.filter_by(username=username).first()

        if user and user.authenticate(password):
            session['user_id'] = user.id
            return {
                "id": user.id,
                "username": user.username,
                "role": user.role
            }, 200
        return {"error": "Invalid username or password"}, 401

class Logout(Resource):
    def delete(self):
        user_id = session.pop('user_id', None)

        if not user_id:
            return {"error": "Unauthorized"}, 401

        return {}, 204


# User views
class Users(Resource):
    def get(self):
        user = authorize()

        if not user:
            return {"error": "Unauthorized"}, 401
        
        if user.role != "admin":
            return {"error": "Forbidden"}, 403

        users = User.query.all()
        return [u.to_dict() for u in users], 200

class UserByID(Resource):
    def get(self, id):
        user = db.session.get(User, id)
        if not user:
            return {"error": "User not found"}, 404

        response_dict = {
            "id": user.id,
            "username": user.username,
            "name": user.name,
            "email": user.email,
            "role": user.role,
            "medication_logs": []
        }

        for ml in user.medication_logs:
            medication_logs_dict = {
                "id": ml.id,
                "medication_name": ml.medication_name,
                "dosage": ml.dosage,
                "time_given": ml.time_given.isoformat() if ml.time_given else None,
                "medication_start": ml.medication_start.isoformat() if ml.medication_start else None,
                "medication_end": ml.medication_end.isoformat() if ml.medication_end else None,
                "frequency": ml.frequency,
                "notes": ml.notes,
                "user_id": ml.user_id,
                "pet_id": ml.pet_id,
                "pet": {
                    "id": ml.pet.id,
                    "name": ml.pet.name,
                    "breed": ml.pet.breed,
                    "age": ml.pet.age,
                    "adoption_status": ml.pet.adoption_status,
                    "favorite_toy": ml.pet.favorite_toy,
                    "favorite_treat": ml.pet.favorite_treat,
                }
            }
            response_dict["medication_logs"].append(medication_logs_dict)

        return response_dict, 200

    def patch(self, id):
        return ''

    def delete(self, id):
        user = authorize()
        if not user:
            return {"error": "Unauthorized"}, 401

        if user.role != "admin":
            return {"error": "Forbidden"}, 403

        u = User.query.get_or_404(id)
        db.session.delete(u)
        db.session.commit()
        return {}, 204

# Pet views
class Pets(Resource):
    def get(self):
        response_dict_list = [p.to_dict() for p in Pet.query.all()]
        return response_dict_list

    def post(self):
        data = request.get_json() or {}

        return ''

class PetByID(Resource):
    def get(self, id):

        pet = db.session.get(Pet, id)

        if not pet:
            return {"error": "Pet not found"}, 404

        response_dict = {
            "id": pet.id,
            "name": pet.name,
            "breed": pet.breed,
            "age": pet.age,
            "sex": pet.sex,
            "weight": pet.weight,
            "date_of_birth": pet.date_of_birth.isoformat() if pet.date_of_birth else None,
            "dob_estimated": pet.dob_estimated,
            "origin_location": pet.origin_location,
            "intake_date": pet.intake_date.isoformat() if pet.intake_date else None,
            "adoption_status": pet.adoption_status,
            "favorite_toy": pet.favorite_toy,
            "favorite_treat": pet.favorite_treat,
            "notes": pet.notes,
            "medication_logs": []
        }

        for ml in pet.medication_logs:
            medication_logs_dict = {
                "id": ml.id,
                "medication_name": ml.medication_name,
                "dosage": ml.dosage,
                "time_given": ml.time_given.isoformat() if ml.time_given else None,
                "medication_start": ml.medication_start.isoformat() if ml.medication_start else None,
                "medication_end": ml.medication_end.isoformat() if ml.medication_end else None,
                "frequency": ml.frequency,
                "notes": ml.notes,
                "user_id": ml.user_id,
                "pet_id": ml.pet_id,
            }

            response_dict["medication_logs"].append(medication_logs_dict)

        return response_dict, 200

    def patch(self, id):
        return ''

    def delete(self, id):
        pet = db.session.get(Pet, id)

        if not pet:
            return {"error": "Pet not found"}, 404

        db.session.delete(pet)
        db.session.commit()

        return '', 204

# Pet image upload views
class PetImageByID(Resource):

    def get(self, pet_id):
        pet = db.session.get(Pet, pet_id)

        if not pet or not pet.profile_image:
            return {"error": f"No image found for {pet_id}"}, 404
        return send_from_directory(app.config['IMAGES_FOLDER'], pet.profile_image)

    def post(self, pet_id):
        pet = db.session.get(Pet, pet_id)
        if not pet:
            return {"error": f"Pet with id {pet_id} not found"}, 404

        if 'file' not in request.files:
            return {"error": "No file part"}, 400

        file = request.files['file']
        if file.filename == '':
            return {"error": "No selected file"}, 400
        if not allowed_file(file.filename):
            return {"error": "File type not allowed"}, 400

        # Save file
        filename = f"{pet.id}_{secure_filename(file.filename)}"
        file_path = os.path.join(app.config['IMAGES_FOLDER'], filename)
        file.save(file_path)

        # Update image
        pet.profile_image = filename
        db.session.commit()

        return {
            "message": "Image uploaded successfully!",
            "profile_image": f"/images/{filename}"
        }, 201

    def patch(self, pet_id):
        pet = db.session.get(Pet, pet_id)
        if not pet:
            return {"error": "Pet not found"}, 404

        if 'file' not in request.files:
            return {"error": "No file part"}, 400

        file = request.files['file']
        if file.filename == '':
            return {"error": "No selected file"}, 400
        if not allowed_file(file.filename):
            return {"error": "File type not allowed"}, 400

        if pet.profile_image:
            old_path = os.path.join(app.config['IMAGES_FOLDER'], pet.profile_image)
            if os.path.exists(old_path):
                os.remove(old_path)

        # Save file
        filename = f"{pet.id}_{secure_filename(file.filename)}"
        file_path = os.path.join(app.config['IMAGES_FOLDER'], filename)
        file.save(file_path)

        # Update image
        pet.profile_image = filename
        db.session.commit()

        return {
            "message": "Image updated successfully!",
            "profile_image": f"/images/{filename}"
        }, 200

    def delete(self, pet_id):
        pet = db.session.get(Pet, pet_id)

        if not pet or not pet.profile_image:
            return {"error": "Image not found"}, 404

        old_path = os.path.join(app.config['IMAGES_FOLDER'], pet.profile_image)
        if os.path.exists(old_path):
            os.remove(old_path)

        pet.profile_image = None
        db.session.commit()

        return '', 204

class PetImageByFilename(Resource):
    def get(self, filename):
        return send_from_directory(app.config['IMAGES_FOLDER'], filename)


# Medication Log views
class MedicationLogs(Resource):
    def get(self):
        return ''

    def post(self):
        return ''

class MedicationLogByID(Resource):
    def patch(self, id):
        return ''

    def delete(self, id):
        return ''



api.add_resource(Signup, '/signup') 
api.add_resource(CheckSession, '/check_session')   
api.add_resource(Login, '/login')    
api.add_resource(Logout, '/logout')

api.add_resource(Users, '/users')
api.add_resource(UserByID, '/users/<int:id>')

api.add_resource(Pets, '/pets')
api.add_resource(PetByID, '/pets/<int:id>')

api.add_resource(PetImageByID, '/pets/<int:pet_id>/image')
api.add_resource(PetImageByFilename, '/images/<string:filename>')

api.add_resource(MedicationLogs, '/medication_logs')
api.add_resource(MedicationLogByID, '/medication_logs/<int:id>')


if __name__ == '__main__':
    app.run(port=5555, debug=True)

