from flask import Blueprint, request, jsonify, session
from datetime import datetime
from src.models import db, Admin

admin_bp = Blueprint('admin', __name__)

@admin_bp.route('/admin/login', methods=['POST'])
def admin_login():
    """Admin login"""
    try:
        data = request.get_json()
        email = data.get('email')
        password = data.get('password')
        
        if not email or not password:
            return jsonify({
                'success': False,
                'message': 'Email and password are required'
            }), 400
        
        # Find admin user
        admin = Admin.query.filter_by(email=email, is_active=True).first()
        
        if not admin or not admin.check_password(password):
            return jsonify({
                'success': False,
                'message': 'Invalid email or password'
            }), 401
        
        # Update last login
        admin.update_last_login()
        db.session.commit()
        
        # Store admin session
        session['admin_id'] = admin.id
        session['admin_email'] = admin.email
        session['is_super_admin'] = admin.is_super_admin
        
        return jsonify({
            'success': True,
            'message': 'Login successful',
            'data': {
                'admin': admin.to_dict(),
                'session_id': session.get('admin_id')
            }
        })
        
    except Exception as e:
        return jsonify({
            'success': False,
            'message': f'Login error: {str(e)}'
        }), 500

@admin_bp.route('/admin/logout', methods=['POST'])
def admin_logout():
    """Admin logout"""
    try:
        session.clear()
        return jsonify({
            'success': True,
            'message': 'Logout successful'
        })
    except Exception as e:
        return jsonify({
            'success': False,
            'message': f'Logout error: {str(e)}'
        }), 500

@admin_bp.route('/admin/profile', methods=['GET'])
def get_admin_profile():
    """Get current admin profile"""
    try:
        admin_id = session.get('admin_id')
        if not admin_id:
            return jsonify({
                'success': False,
                'message': 'Not authenticated'
            }), 401
        
        admin = Admin.query.get(admin_id)
        if not admin:
            return jsonify({
                'success': False,
                'message': 'Admin not found'
            }), 404
        
        return jsonify({
            'success': True,
            'data': admin.to_dict()
        })
        
    except Exception as e:
        return jsonify({
            'success': False,
            'message': f'Error fetching profile: {str(e)}'
        }), 500

@admin_bp.route('/admin/change-password', methods=['POST'])
def change_admin_password():
    """Change admin password"""
    try:
        admin_id = session.get('admin_id')
        if not admin_id:
            return jsonify({
                'success': False,
                'message': 'Not authenticated'
            }), 401
        
        data = request.get_json()
        current_password = data.get('current_password')
        new_password = data.get('new_password')
        
        if not current_password or not new_password:
            return jsonify({
                'success': False,
                'message': 'Current password and new password are required'
            }), 400
        
        admin = Admin.query.get(admin_id)
        if not admin:
            return jsonify({
                'success': False,
                'message': 'Admin not found'
            }), 404
        
        # Verify current password
        if not admin.check_password(current_password):
            return jsonify({
                'success': False,
                'message': 'Current password is incorrect'
            }), 400
        
        # Update password
        admin.set_password(new_password)
        db.session.commit()
        
        return jsonify({
            'success': True,
            'message': 'Password changed successfully'
        })
        
    except Exception as e:
        db.session.rollback()
        return jsonify({
            'success': False,
            'message': f'Error changing password: {str(e)}'
        }), 500

@admin_bp.route('/admin/users', methods=['GET'])
def get_admin_users():
    """Get all admin users (Super Admin only)"""
    try:
        admin_id = session.get('admin_id')
        if not admin_id:
            return jsonify({
                'success': False,
                'message': 'Not authenticated'
            }), 401
        
        current_admin = Admin.query.get(admin_id)
        if not current_admin or not current_admin.is_super_admin:
            return jsonify({
                'success': False,
                'message': 'Access denied. Super admin privileges required'
            }), 403
        
        admins = Admin.query.all()
        return jsonify({
            'success': True,
            'data': [admin.to_dict() for admin in admins]
        })
        
    except Exception as e:
        return jsonify({
            'success': False,
            'message': f'Error fetching admin users: {str(e)}'
        }), 500

@admin_bp.route('/admin/users', methods=['POST'])
def create_admin_user():
    """Create new admin user (Super Admin only)"""
    try:
        admin_id = session.get('admin_id')
        if not admin_id:
            return jsonify({
                'success': False,
                'message': 'Not authenticated'
            }), 401
        
        current_admin = Admin.query.get(admin_id)
        if not current_admin or not current_admin.is_super_admin:
            return jsonify({
                'success': False,
                'message': 'Access denied. Super admin privileges required'
            }), 403
        
        data = request.get_json()
        
        # Validate required fields
        required_fields = ['email', 'password', 'full_name']
        for field in required_fields:
            if not data.get(field):
                return jsonify({
                    'success': False,
                    'message': f'Field {field} is required'
                }), 400
        
        # Check if admin already exists
        existing = Admin.query.filter_by(email=data['email']).first()
        if existing:
            return jsonify({
                'success': False,
                'message': 'Admin with this email already exists'
            }), 400
        
        # Create new admin
        admin = Admin(
            email=data['email'],
            full_name=data['full_name'],
            is_super_admin=data.get('is_super_admin', False)
        )
        admin.set_password(data['password'])
        
        db.session.add(admin)
        db.session.commit()
        
        return jsonify({
            'success': True,
            'message': 'Admin user created successfully',
            'data': admin.to_dict()
        }), 201
        
    except Exception as e:
        db.session.rollback()
        return jsonify({
            'success': False,
            'message': f'Error creating admin user: {str(e)}'
        }), 500

@admin_bp.route('/admin/users/<int:user_id>', methods=['PUT'])
def update_admin_user(user_id):
    """Update admin user (Super Admin only)"""
    try:
        admin_id = session.get('admin_id')
        if not admin_id:
            return jsonify({
                'success': False,
                'message': 'Not authenticated'
            }), 401
        
        current_admin = Admin.query.get(admin_id)
        if not current_admin or not current_admin.is_super_admin:
            return jsonify({
                'success': False,
                'message': 'Access denied. Super admin privileges required'
            }), 403
        
        admin = Admin.query.get_or_404(user_id)
        data = request.get_json()
        
        # Update fields
        if 'full_name' in data:
            admin.full_name = data['full_name']
        if 'is_active' in data:
            admin.is_active = data['is_active']
        if 'is_super_admin' in data:
            admin.is_super_admin = data['is_super_admin']
        
        db.session.commit()
        
        return jsonify({
            'success': True,
            'message': 'Admin user updated successfully',
            'data': admin.to_dict()
        })
        
    except Exception as e:
        db.session.rollback()
        return jsonify({
            'success': False,
            'message': f'Error updating admin user: {str(e)}'
        }), 500

@admin_bp.route('/admin/check-auth', methods=['GET'])
def check_admin_auth():
    """Check if admin is authenticated"""
    try:
        admin_id = session.get('admin_id')
        if not admin_id:
            return jsonify({
                'success': False,
                'authenticated': False,
                'message': 'Not authenticated'
            }), 401
        
        admin = Admin.query.get(admin_id)
        if not admin or not admin.is_active:
            session.clear()
            return jsonify({
                'success': False,
                'authenticated': False,
                'message': 'Admin account not found or inactive'
            }), 401
        
        return jsonify({
            'success': True,
            'authenticated': True,
            'data': admin.to_dict()
        })
        
    except Exception as e:
        return jsonify({
            'success': False,
            'authenticated': False,
            'message': f'Authentication check error: {str(e)}'
        }), 500

