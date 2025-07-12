#!/usr/bin/env python3
"""
Database initialization script for State Bangladesh Society
This script creates default categories and admin user
"""

import os
import sys
sys.path.insert(0, os.path.dirname(__file__))

from src.main import app
from src.models import db, Category, Admin

def init_database():
    """Initialize database with default data"""
    with app.app_context():
        # Create all tables
        db.create_all()
        
        # Check if categories already exist
        if Category.query.count() == 0:
            # Create default categories
            default_categories = [
                {
                    'name': 'Housing Project',
                    'description': 'Applications for housing assistance and development projects'
                },
                {
                    'name': 'Tube Well Project',
                    'description': 'Applications for tube well installation and water supply projects'
                },
                {
                    'name': 'Education Support',
                    'description': 'Applications for educational assistance and scholarship programs'
                },
                {
                    'name': 'Healthcare Support',
                    'description': 'Applications for healthcare assistance and medical support'
                },
                {
                    'name': 'Agricultural Support',
                    'description': 'Applications for agricultural development and farming assistance'
                },
                {
                    'name': 'Small Business Support',
                    'description': 'Applications for small business development and microfinance'
                }
            ]
            
            for cat_data in default_categories:
                category = Category(**cat_data)
                db.session.add(category)
            
            print("✓ Default categories created")
        
        # Check if admin user already exists
        if Admin.query.count() == 0:
            # Create default admin user
            admin = Admin(
                email='admin@statebd.org',
                full_name='System Administrator',
                is_super_admin=True
            )
            admin.set_password('admin123')  # Default password - should be changed
            db.session.add(admin)
            
            print("✓ Default admin user created")
            print("  Email: admin@statebd.org")
            print("  Password: admin123")
            print("  ⚠️  Please change the default password after first login!")
        
        # Commit all changes
        db.session.commit()
        print("✓ Database initialization completed successfully!")

if __name__ == '__main__':
    init_database()

