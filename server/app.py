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
    public_endpoints = ['index', 'Signup', 'Login', 'CheckSession']
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
        user.set_password(data['password'])

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
        return ''

class Logout(Resource):
    def delete(self):
        return ''


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
        return ''

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
        return ''

    def post(self):
        return ''

class PetByID(Resource):
    def get(self, id):
        return ''

    def patch(self, id):
        return ''

    def delete(self, id):
        return ''

# Pet image upload views
class PetImageUpload(Resource):
    def post(self, pet_id):
        pet = Pet.query.get(pet_id)
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

class PetImageResource(Resource):
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

api.add_resource(PetImageUpload, '/pets/<int:pet_id>/upload_image')
api.add_resource(PetImageResource, '/images/<string:filename>')

api.add_resource(MedicationLogs, '/medication_logs')
api.add_resource(MedicationLogByID, '/medication_logs/<int:id>')


if __name__ == '__main__':
    app.run(port=5555, debug=True)

