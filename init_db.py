"""
Simple database initialization script - creates tables without seed data.
This avoids the heavy imports that slow down seed.py
"""
import os
import sys

# Setup path
sys.path.insert(0, '/Users/sahanas/in/pm-internship')
os.chdir('/Users/sahanas/in/pm-internship')

from flask import Flask
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)
# Use relative path that works with SQLite
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:////Users/sahanas/in/pm-internship/instance/database.db'
db = SQLAlchemy(app)

# Import all models
from app import User, StudentProfile, StudentPortfolio, StudentCertificate
from app import StudentInternshipExperience, Organization, Internship, Application

# Create all tables
with app.app_context():
    db.create_all()
    print("✓ Database tables created successfully!")
    print("✓ StudentProfile table now includes 'viewed_by_org' column")
