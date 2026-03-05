from config import db, bcrypt
from sqlalchemy.orm import validates
from sqlalchemy.ext.hybrid import hybrid_property
from sqlalchemy.ext.associationproxy import association_proxy
from sqlalchemy_serializer import SerializerMixin
from datetime import date, datetime

# Models
class User(db.Model, SerializerMixin):
  __tablename__ = "users"

  id = db.Column(db.Integer, primary_key=True) 
  username = db.Column(db.String, nullable=False, unique=True)
  name = db.Column(db.String, nullable=False)
  email = db.Column(db.String, nullable=False, unique=True)
  _password_hash = db.Column(db.String, nullable=False)
  role = db.Column(db.String, nullable=False)

  created_at = db.Column(db.DateTime, default=datetime.utcnow)
  updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

  # Relationships
  medication_logs = db.relationship("MedicationLog", back_populates="user", cascade="all, delete-orphan")
  pets = association_proxy('medication_logs', 'pet')

  # Serialization rules
  serialize_rules = ('-_password_hash', '-medication_logs.user', '-medication_logs.pet')

  # Password property
  @hybrid_property
  def password_hash(self):
    raise AttributeError('Password hashes may not be viewed.')

  @password_hash.setter
  def password_hash(self, password):
    if not password or len(password) < 8:
      raise ValueError("Password must be at least 8 characters")
    pw_hash = bcrypt.generate_password_hash(password.encode('utf-8'))
    self._password_hash = pw_hash.decode('utf-8')

  def authenticate(self, password):
    return bcrypt.check_password_hash(
      self._password_hash, password.encode('utf-8'))

  # Validations
  @validates("email")
  def validate_email(self, key, value):
    if "@" not in value:
      raise ValueError("Invalid email")
    return value

  @validates("_password_hash")
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
  profile_image = db.Column(db.String)

  created_at = db.Column(db.DateTime, default=datetime.utcnow)
  updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

  # Relationships
  medication_logs = db.relationship("MedicationLog", back_populates="pet", cascade="all, delete-orphan")
  users = association_proxy('medication_logs', 'user')

  # Serialization rules
  serialize_rules = ('-medication_logs.pet', '-medication_logs.user')

  # Validations
  @validates("name", "breed", "sex", "weight", "origin_location", "adoption_status")
  def validate_not_empty(self, key, value):
      if not value or str(value).strip() == "":
        raise ValueError(f"{key} cannot be empty")
      return value

  @validates("age")
  def validate_age(self, key, value):
      if value is not None and value < 0:
          raise ValueError("Age cannot be negative")
      return value

  @validates("date_of_birth", "dob_estimated", "intake_date")
  def validate_dates(self, key, value):
    if value is not None and not isinstance(value, (date, datetime)):
      raise ValueError(f"{key} must be a date or datetime object")
    return value

  def __repr__(self):
    return f"<Pet {self.name}, {self.breed}>"


class MedicationLog(db.Model, SerializerMixin):
  __tablename__ = "medication_logs"

  id = db.Column(db.Integer, primary_key=True)
  # Foreign keys
  user_id = db.Column(db.Integer, db.ForeignKey("users.id", ondelete="CASCADE"), nullable=False)
  pet_id = db.Column(db.Integer, db.ForeignKey("pets.id", ondelete="CASCADE"), nullable=False)

  medication_name = db.Column(db.String, nullable=False)
  dosage = db.Column(db.String, nullable=False)
  time_given = db.Column(db.DateTime, nullable=False)
  medication_start = db.Column(db.Date, nullable=False)
  medication_end = db.Column(db.Date, nullable=False)
  frequency = db.Column(db.String, nullable=False)
  notes = db.Column(db.String, nullable=False)

  created_at = db.Column(db.DateTime, default=datetime.utcnow)
  updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

  # Relationships
  user = db.relationship("User", back_populates="medication_logs")
  pet = db.relationship("Pet", back_populates="medication_logs")

  # Serialization rules
  serialize_rules = ('-user.medication_logs', '-pet.medication_logs')

  # Validations
  @validates("medication_name", "dosage", "frequency")
  def validate_non_empty(self, key, value):
    if not value or str(value).strip() == "":
      raise ValueError(f"{key} cannot be empty")
    return value

  @validates("time_given", "medication_start", "medication_end")
  def validate_dates(self, key, value):
    if value is not None and not isinstance(value, (date, datetime)):
      raise ValueError(f"{key} must be a date or datetime object")
    return value