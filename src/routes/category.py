from flask import Blueprint, request, jsonify
from src.models import db, Category

category_bp = Blueprint('category', __name__)

@category_bp.route('/categories', methods=['GET'])
def get_categories():
    """Get all active categories"""
    try:
        categories = Category.query.filter_by(is_active=True).all()
        return jsonify({
            'success': True,
            'data': [category.to_dict() for category in categories]
        })
    except Exception as e:
        return jsonify({
            'success': False,
            'message': f'Error fetching categories: {str(e)}'
        }), 500

@category_bp.route('/categories/<int:category_id>', methods=['GET'])
def get_category(category_id):
    """Get a specific category by ID"""
    try:
        category = Category.query.get_or_404(category_id)
        return jsonify({
            'success': True,
            'data': category.to_dict()
        })
    except Exception as e:
        return jsonify({
            'success': False,
            'message': f'Error fetching category: {str(e)}'
        }), 500

@category_bp.route('/categories', methods=['POST'])
def create_category():
    """Create a new category (Admin only)"""
    try:
        data = request.get_json()
        
        # Validate required fields
        if not data.get('name'):
            return jsonify({
                'success': False,
                'message': 'Category name is required'
            }), 400
        
        # Check if category already exists
        existing = Category.query.filter_by(name=data['name']).first()
        if existing:
            return jsonify({
                'success': False,
                'message': 'Category with this name already exists'
            }), 400
        
        # Create new category
        category = Category(
            name=data['name'],
            description=data.get('description', ''),
            is_active=data.get('is_active', True)
        )
        
        db.session.add(category)
        db.session.commit()
        
        return jsonify({
            'success': True,
            'message': 'Category created successfully',
            'data': category.to_dict()
        }), 201
        
    except Exception as e:
        db.session.rollback()
        return jsonify({
            'success': False,
            'message': f'Error creating category: {str(e)}'
        }), 500

@category_bp.route('/categories/<int:category_id>', methods=['PUT'])
def update_category(category_id):
    """Update a category (Admin only)"""
    try:
        category = Category.query.get_or_404(category_id)
        data = request.get_json()
        
        # Update fields
        if 'name' in data:
            category.name = data['name']
        if 'description' in data:
            category.description = data['description']
        if 'is_active' in data:
            category.is_active = data['is_active']
        
        db.session.commit()
        
        return jsonify({
            'success': True,
            'message': 'Category updated successfully',
            'data': category.to_dict()
        })
        
    except Exception as e:
        db.session.rollback()
        return jsonify({
            'success': False,
            'message': f'Error updating category: {str(e)}'
        }), 500

@category_bp.route('/categories/<int:category_id>', methods=['DELETE'])
def delete_category(category_id):
    """Delete a category (Admin only)"""
    try:
        category = Category.query.get_or_404(category_id)
        
        # Soft delete by setting is_active to False
        category.is_active = False
        db.session.commit()
        
        return jsonify({
            'success': True,
            'message': 'Category deleted successfully'
        })
        
    except Exception as e:
        db.session.rollback()
        return jsonify({
            'success': False,
            'message': f'Error deleting category: {str(e)}'
        }), 500

