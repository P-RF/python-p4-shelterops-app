# Standard library imports
import os

# Remote library imports
from flask import Flask
from flask_bcrypt import Bcrypt
from flask_cors import CORS
from flask_migrate import Migrate
from flask_restful import Api
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import MetaData

# Local imports

# Instantiate app
app = Flask(__name__)

# Config values
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///app.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.json.compact = False
app.config['SECRET_KEY'] = os.environ.get("SECRET_KEY", "supersecretkey")

# Images folder
BASE_DIR = os.getcwd()
app.config['IMAGES_FOLDER'] = os.path.join(BASE_DIR, "images")

# SQLAlchemy Metadata and db
metadata = MetaData(naming_convention={
    "fk": "fk_%(table_name)s_%(column_0_name)s_%(referred_table_name)s",
})
db = SQLAlchemy(metadata=metadata)
db.init_app(app)

# Flask extensions
migrate = Migrate(app, db)
bcrypt = Bcrypt(app)
api = Api(app)

# CORS
FRONTEND_URLS = [
    "http://localhost:4000", # dev
    "http://localhost:5000", # dev
]
CORS(app, resources={r"/api/*": {"origins": FRONTEND_URLS}})