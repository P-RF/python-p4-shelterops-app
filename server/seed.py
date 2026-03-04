#!/usr/bin/env python3

# Standard library imports
from datetime import date, datetime

# Remote library imports

# Local imports
from app import app
from models import db, User, Pet, MedicationLog

with app.app_context():

    print("Deleting data...")
    MedicationLog.query.delete()
    Pet.query.delete()
    User.query.delete()

    print("Creating users...")
    staff = User(
        username="simon_99", 
        name="Simon", 
        email="simon_99@email.com", 
        role="staff")
    staff.set_password("password123")

    admin = User(
        username="sarah123", 
        name="Sarah", 
        email="sarah123@email.com", 
        role="admin")
    admin.set_password("password123")

    volunteer = User(
        username="michelle.87", 
        name="Michelle", 
        email="michelle.87@email.com", 
        role="volunteer")
    volunteer.set_password("password123")

    users = [staff, admin, volunteer]
    db.session.add_all(users)
    db.session.commit()


    print("Creating pets...")
    dog = Pet(
        name="Buddy", 
        breed="Golden Retriever", 
        age=3, 
        sex="Male", 
        weight="65 lbs", 
        date_of_birth=date(2022, 2, 22) , 
        dob_estimated=None, 
        origin_location="Cleveland, Ohio", 
        intake_date=date(2025, 7, 15), 
        adoption_status="Available", 
        favorite_toy="Rubber Duck", 
        favorite_treat="Pumpkin Biscuits", 
        notes="", 
        profile_image="https://www.goldenrescue.com/wp-content/uploads/2024/08/16.jpg")

    cat = Pet(
        name="Sr. Agave", 
        breed="Aztec Cat", 
        age=7, 
        sex="Male", 
        weight="10 lbs", 
        date_of_birth=date(2018, 4, 5), 
        dob_estimated=None, 
        origin_location="Austin, Texas", 
        intake_date=date(2025, 11, 19), 
        adoption_status="Adopted", 
        favorite_toy="Mini Slinky", 
        favorite_treat="Lickables (Tuna)", 
        notes="", 
        profile_image="https://www.kimballstock.com/pix/ani/p/02/cat-02-rk0468-03p.jpg")

    rabbit = Pet(
        name="Bugs", 
        breed="Holland Lop", 
        age=5, 
        sex="Male", 
        weight="15 lbs", 
        date_of_birth=date(2020, 7, 29), 
        dob_estimated=None, 
        origin_location="Charleston, South Carolina", 
        intake_date=date(2025, 5, 10), 
        adoption_status="Available", 
        favorite_toy="Willow Ball", 
        favorite_treat="Carrots", 
        notes="", 
        profile_image="https://images.squarespace-cdn.com/content/v1/54ff9a97e4b063025cf9895c/1497567728318-JV19ETXBKJ3RB2UXGORK/DSC_6655.JPG")

    bird = Pet(
        name="Polly", 
        breed="African Grey", 
        age=18, 
        sex="Female", 
        weight="17 oz", 
        date_of_birth=None , 
        dob_estimated=date(2007, 12, 24), 
        origin_location="Wilmington, Delaware", 
        intake_date=date(2025, 9, 26), 
        adoption_status="Pending", 
        favorite_toy="Popsicle Sticks", 
        favorite_treat="Pomegranate", 
        notes="", 
        profile_image="https://encrypted-tbn0.gstatic.com/images?q=tbn:ANd9GcTsM8OiDEOSFElkpqaLDZOKfHIck48wfudFQg&s")
    
    pets = [dog, cat, rabbit, bird]
    db.session.add_all(pets)
    db.session.commit()


    print("Creating MedicationLog...")
    ml1 = MedicationLog(
        user_id=staff.id, 
        pet_id=dog.id, 
        medication_name="Rimadyl (Caprofen)", 
        dosage="25 mg PO daily", 
        time_given=datetime(2025, 12, 30, 9, 0), 
        medication_start=date(2025, 12, 30), 
        medication_end=date(2026, 1, 9), 
        frequency="Daily", 
        notes="with treat")

    ml2 = MedicationLog(
        user_id=admin.id, 
        pet_id=cat.id, 
        medication_name="Heartgard (Invermectin)", 
        dosage="6 mg PO monthly", 
        time_given=datetime(2025, 11, 12, 8, 30), 
        medication_start=date(2025, 11, 12), 
        medication_end=date(2099, 12, 31), 
        frequency="Monthly", 
        notes="")

    ml3 = MedicationLog(
        user_id=volunteer.id, 
        pet_id=rabbit.id, 
        medication_name="Benadryl", 
        dosage="0.1 ml PO twice daily", 
        time_given=datetime(2025, 7, 18, 16, 25), 
        medication_start=date(2025, 7, 18), 
        medication_end=date(2025, 7, 28), 
        frequency="Twice Daily", 
        notes="Children's Benadryl only. Give treat after.")
    
    medicationLogs = [ml1, ml2, ml3]
    db.session.add_all(medicationLogs)
    db.session.commit()

    print("Seeding complete!")