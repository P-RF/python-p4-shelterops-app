#!/usr/bin/env python3

# Standard library imports
import os

# Remote library imports
from flask import request, send_from_directory
from flask_restful import Resource
from werkzeug.utils import secure_filename

# Local imports
from config import app, db, api

# Check if images exist
os.makedirs(app.config['IMAGES_FOLDER'], exist_ok=True)

# Allow image extensions
ALLOWED_EXTENSIONS = {'png', 'jpg', 'jpeg', 'gif'}
def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

# Add your model imports
from models import User, Pet, MedicationLog

# Views go here!
@app.route('/')
def index():
    return '<h1>Project Server</h1>'

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

    
api.add_resource(PetImageUpload, '/pets/<int:pet_id>/upload_image')
api.add_resource(PetImageResource, '/images/<string:filename>')


if __name__ == '__main__':
    app.run(port=5555, debug=True)

