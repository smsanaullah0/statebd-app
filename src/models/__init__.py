from flask_sqlalchemy import SQLAlchemy

# Initialize the database instance
db = SQLAlchemy()

# Import all models
from .user import User
from .category import Category
from .application import Application
from .admin import Admin

# Make models available for import
__all__ = ['db', 'User', 'Category', 'Application', 'Admin']

