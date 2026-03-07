#!/usr/bin/env python3

# Standard library imports
import os
from datetime import datetime

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
    return db.session.get(User, user_id)

@app.before_request
def check_if_logged_in():
    public_endpoints = ['index', 'signup', 'login', 'check_session']
    if request.endpoint in public_endpoints:
        return
    if not session.get('user_id'):
        return {"error" : "Unauthorized"}, 401

# Authorization endpoints
class Signup(Resource):
    def post(self):
        data = request.get_json() or {}

        username = data.get('username')
        email = data.get('email')

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

        if username and User.query.filter(db.func.lower(User.username) == username.lower()).first():
            errors.append("Username already exists")
        if email and User.query.filter(db.func.lower(User.email) == email.lower()).first():
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
        data = request.get_json() or  {}

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
        current_user = authorize()

        if not current_user:
            return {"error": "Unauthorized"}, 401
        
        if current_user.role != "admin":
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
        current_user = authorize()
        if not current_user:
            return {"error": "Unauthorized"}, 401

        if current_user.role != "admin":
            return {"error": "Forbidden"}, 403

        user = db.session.get(User, id)
        if not user:
            return {"error": "User not found"}, 404

        data = request.get_json() or {}

        if 'username' in data:
            if User.query.filter(db.func.lower(User.username) == data['username'].lower(), User.id != user.id).first():
                return {"error": "Username already exists"}, 422
            user.username = data['username']
            
        if 'email' in data:
            if User.query.filter(db.func.lower(User.email) == data['email'].lower(), User.id != user.id).first():
                return {"error": "Email already exists"}, 422
            user.email = data['email']

        if 'name' in data:
            user.name = data['name']
        if 'role' in data:
            user.role = data['role']
        if 'password' in data:
            user.password_hash = data['password']

        db.session.commit()
        return user.to_dict(), 200

    def delete(self, id):
        current_user = authorize()
        if not current_user:
            return {"error": "Unauthorized"}, 401

        # Only admin can delete a user
        if current_user.role != "admin":
            return {"error": "Forbidden"}, 403

        user = db.session.get(User, id)
        if not user:
            return {"error": "User not found"}, 404

        db.session.delete(user)
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
        current_user = authorize()
        if not current_user:
            return {"error": "Unauthorized"}, 401

        if current_user.role not in ["admin", "staff"]:
            return {"error": "Only admin or staff can delete pets"}, 403
        
        pet = db.session.get(Pet, id)
        if not pet:
            return {"error": "Pet not found"}, 404

        db.session.delete(pet)
        db.session.commit()
        return {}, 204

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
        ml_dict_list = [ml.to_dict() for ml in MedicationLog.query.all()]
        return ml_dict_list, 200

    def post(self):
        current_user = authorize()
        if not current_user:
            return {"error": "Unauthorized"}, 401

        data = request.get_json() or {}

        user_id = data.get("user_id")
        pet_id = data.get("pet_id")
        medication_name = data.get("medication_name")

        user = db.session.get(User, user_id)
        pet = db.session.get(Pet, pet_id)

        # Validation
        if not user or not pet or not medication_name:
            return {"errors": ["Invalid user, pet, or medication_name"]}, 400

        time_given = datetime.fromisoformat(data["time_given"]) if data.get("time_given") else None
        medication_start = datetime.fromisoformat(data["medication_start"]).date() if data.get("medication_start") else None
        medication_end = datetime.fromisoformat(data["medication_end"]).date() if data.get("medication_end") else None

        new_ml = MedicationLog(
            user_id = data.get("user_id"),
            pet_id = data.get("pet_id"),
            medication_name = data.get("medication_name"),
            dosage = data.get("dosage"),
            time_given=time_given,
            medication_start=medication_start,
            medication_end=medication_end,
            frequency = data.get("frequency"),
            notes = data.get("notes")
        )
        db.session.add(new_ml)
        db.session.commit()

        response_dict = {
            "id": new_ml.id,
            "medication_name": new_ml.medication_name,
            "dosage": new_ml.dosage,
            "time_given": new_ml.time_given.isoformat() if new_ml.time_given else None,
            "medication_start": new_ml.medication_start.isoformat() if new_ml.medication_start else None,
            "medication_end": new_ml.medication_end.isoformat() if new_ml.medication_end else None,
            "frequency": new_ml.frequency,
            "notes": new_ml.notes,
            "pet": {
                "id": pet.id,
                "name": pet.name,
                "breed": pet.breed,
                "age": pet.age,
                "adoption_status": pet.adoption_status,
                "favorite_toy": pet.favorite_toy,
                "favorite_treat": pet.favorite_treat,
            },
            "user": {
                "id": user.id,
                "username": user.username,
                "name": user.name,
                "email": user.email,
                "role": user.role
            }
        }
        return response_dict, 201

class MedicationLogByID(Resource):
    def patch(self, id):
        current_user = authorize()
        if not current_user:
            return {"error": "Unauthorized"}, 401

        ml = db.session.get(MedicationLog, id)
        if not ml:
            return {"error": "Medication log not found"}, 404

        data = request.get_json() or {}

        if 'medication_name' in data:
            ml.medication_name = data['medication_name']
        if 'dosage' in data:
            ml.dosage = data['dosage']
        if 'time_given' in data:
            ml.time_given = datetime.fromisoformat(data['time_given']) if data['time_given'] else None
        if 'medication_start' in data:
            ml.medication_start = datetime.fromisoformat(data['medication_start']).date() if data['medication_start'] else None
        if 'medication_end' in data:
            ml.medication_end = datetime.fromisoformat(data['medication_end']).date() if data['medication_end'] else None
        if 'frequency' in data:
            ml.frequency = data['frequency']
        if 'notes' in data:
            ml.notes = data['notes']

        db.session.commit()

        return ml.to_dict(), 200

    def delete(self, id):
        current_user = authorize()
        if not current_user:
            return {"error": "Unauthorized"}, 401

        ml = db.session.get(MedicationLog, id)
        if not ml:
            return {"error": "Medication log not found"}, 404

        # Only admin can delete a log
        if current_user.role != "admin":
            return {"error": "Unauthorized to delete log"}, 403

        db.session.delete(ml)
        db.session.commit()
        return {}, 204



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

