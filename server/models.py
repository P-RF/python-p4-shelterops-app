from sqlalchemy.orm import validates
from sqlalchemy.ext.associationproxy import association_proxy
from sqlalchemy_serializer import SerializerMixin
from datetime import datetime
from werkzeug.security import generate_password_hash, check_password_hash

from config import db

# Models
class User(db.Model, SerializerMixin):
  __tablename__ = "users"

  id = db.Column(db.Integer, primary_key=True) 
  username = db.Column(db.String, nullable=False, unique=True)
  name = db.Column(db.String, nullable=False)
  email = db.Column(db.String, nullable=False, unique=True)
  password_hash = db.Column(db.String, nullable=False)
  role = db.Column(db.String, nullable=False)

  created_at = db.Column(db.DateTime, default=datetime.utcnow)
  updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

  # Relationships
  medication_logs = db.relationship("MedicationLog", back_populates="user", cascade="all, delete-orphan")
  pets = association_proxy('medication_logs', 'pet')

  # Serialization rules
  serialize_rules = ('-password_hash', '-medication_logs.user', '-medication_logs.pet')

  def set_password(self, password):
    if len(password) < 8:
      raise ValueError("Password must be at least 8 characters")
    self.password_hash = generate_password_hash(password)

  def check_password(self, password):
    return check_password_hash(self.password_hash, password)

  # Validations
  @validates("email")
  def validate_email(self, key, value):
    if "@" not in value:
      raise ValueError("Invalid email")
    return value

  @validates("password_hash")
  def validate_password(self, key, value):
    if not value:
      raise ValueError("Password required")
    return value

  def __repr__(self):
    return f"<User {self.username}>"


class Pet(db.Model, SerializerMixin):
  __tablename__ = "pets"

  id = db.Column(db.Integer, primary_key=True)
  name = db.Column(db.String, nullable=False)
  breed = db.Column(db.String, nullable=False)
  age = db.Column(db.Integer)
  sex = db.Column(db.String, nullable=False)
  weight = db.Column(db.String, nullable=False)
  date_of_birth = db.Column(db.Date)
  dob_estimated = db.Column(db.Date)
  origin_location = db.Column(db.String, nullable=False)
  intake_date = db.Column(db.Date)
  adoption_status = db.Column(db.String, nullable=False)
  favorite_toy = db.Column(db.String)
  favorite_treat = db.Column(db.String)
  notes = db.Column(db.String)

  created_at = db.Column(db.DateTime, default=datetime.utcnow)
  updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

  # Relationships
  medication_logs = db.relationship("MedicationLog", back_populates="pet", cascade="all, delete-orphan")
  users = association_proxy('medication_logs', 'user')

  # Serialization rules
  serialize_rules = ('-medication_logs.pet', '-medication_logs.user')

  # Validations
  @validates("name", "breed", "sex", "weight", "origin_location", "adoption_status")
  def validate_non_empty(self, key, value):
      if not value or str(value).strip() == "":
        raise ValueError(f"{key} cannot be empty")
      return value

  @validates("age")
  def validate_age(self, key, value):
      if value is not None and value < 0:
          raise ValueError("Age cannot be negative")
      return value

  @validates("weight")
  def validate_weight(self, key, value):
    if not value:
      raise ValueError("Weight cannot be empty")
    return value

  @validates("date_of_birth", "dob_estimated", "intake_date")
  def validate_dates(self, key, value):
    if value and not isinstance(value, datetime.date):
      raise ValueError(f"{key} must be a date")
    return value

  def __repr__(self):
    return f"<Pet {self.name}, {self.breed}>"


class MedicationLog(db.Model, SerializerMixin):
  __tablename__ = "medication_logs"

  id = 
  user_id = 
  pet_id = 
  medication_name = 
  dosage = 
  time_given = 
  medication_start = 
  medication_end = 
  frequency = 
  notes = 

  created_at = 
  updated_at = 

  # Relationships


  # Serialization rules


  # Validations