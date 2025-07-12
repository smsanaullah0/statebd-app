from flask import Blueprint, request, jsonify, current_app
from werkzeug.utils import secure_filename
from datetime import datetime
import os
import json
from src.models import db, Application, Category
from src.services import PDFGenerator, EmailService

application_bp = Blueprint('application', __name__)

ALLOWED_EXTENSIONS = {'png', 'jpg', 'jpeg', 'gif', 'pdf', 'doc', 'docx'}

def allowed_file(filename):
    return '.' in filename and \
           filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

def save_uploaded_file(file, folder):
    """Save uploaded file and return the file path"""
    if file and allowed_file(file.filename):
        filename = secure_filename(file.filename)
        # Add timestamp to avoid filename conflicts
        timestamp = datetime.now().strftime('%Y%m%d_%H%M%S_')
        filename = timestamp + filename
        
        upload_path = os.path.join(current_app.config['UPLOAD_FOLDER'], folder)
        os.makedirs(upload_path, exist_ok=True)
        
        file_path = os.path.join(upload_path, filename)
        file.save(file_path)
        return os.path.join(folder, filename)
    return None

@application_bp.route('/applications', methods=['POST'])
def submit_application():
    """Submit a new application"""
    try:
        # Get form data
        data = request.form.to_dict()
        
        # Validate required fields
        required_fields = [
            'full_name', 'father_name', 'mother_name', 'nid_number',
            'date_of_birth', 'occupation', 'village', 'upazila',
            'district', 'division', 'family_members_count',
            'monthly_income', 'main_earner_occupation', 'email',
            'mobile_number', 'category_id'
        ]
        
        for field in required_fields:
            if not data.get(field):
                return jsonify({
                    'success': False,
                    'message': f'Field {field} is required'
                }), 400
        
        # Validate category exists
        category = Category.query.get(data['category_id'])
        if not category or not category.is_active:
            return jsonify({
                'success': False,
                'message': 'Invalid category selected'
            }), 400
        
        # Handle file uploads
        photo_path = None
        signature_path = None
        nid_image_path = None
        other_documents = []
        
        if 'photo' in request.files:
            photo_path = save_uploaded_file(request.files['photo'], 'photos')
        
        if 'signature' in request.files:
            signature_path = save_uploaded_file(request.files['signature'], 'signatures')
        
        if 'nid_image' in request.files:
            nid_image_path = save_uploaded_file(request.files['nid_image'], 'nid_images')
        
        # Handle multiple other documents
        if 'other_documents' in request.files:
            files = request.files.getlist('other_documents')
            for file in files:
                if file and file.filename:
                    doc_path = save_uploaded_file(file, 'documents')
                    if doc_path:
                        other_documents.append({
                            'filename': file.filename,
                            'path': doc_path
                        })
        
        # Create application
        application = Application(
            full_name=data['full_name'],
            father_name=data['father_name'],
            mother_name=data['mother_name'],
            nid_number=data['nid_number'],
            date_of_birth=datetime.strptime(data['date_of_birth'], '%Y-%m-%d').date(),
            occupation=data['occupation'],
            village=data['village'],
            upazila=data['upazila'],
            district=data['district'],
            division=data['division'],
            family_members_count=int(data['family_members_count']),
            monthly_income=float(data['monthly_income']),
            main_earner_occupation=data['main_earner_occupation'],
            email=data['email'],
            mobile_number=data['mobile_number'],
            category_id=int(data['category_id']),
            photo_path=photo_path,
            signature_path=signature_path,
            nid_image_path=nid_image_path,
            other_documents_path=json.dumps(other_documents) if other_documents else None
        )
        
        db.session.add(application)
        db.session.commit()
        
        # Generate and send PDF email
        try:
            pdf_generator = PDFGenerator(current_app.config['UPLOAD_FOLDER'])
            email_service = EmailService()
            
            # Generate PDF bytes
            pdf_bytes = pdf_generator.generate_pdf_bytes(application)
            
            if pdf_bytes:
                # Send email with PDF attachment
                email_service.send_application_confirmation(application, pdf_bytes)
        except Exception as e:
            print(f"Error sending confirmation email: {str(e)}")
            # Don't fail the application submission if email fails
        
        return jsonify({
            'success': True,
            'message': 'Application submitted successfully',
            'data': {
                'reference_number': application.reference_number,
                'application_id': application.id
            }
        }), 201
        
    except Exception as e:
        db.session.rollback()
        return jsonify({
            'success': False,
            'message': f'Error submitting application: {str(e)}'
        }), 500

@application_bp.route('/applications/<reference_number>', methods=['GET'])
def get_application_by_reference(reference_number):
    """Get application by reference number"""
    try:
        application = Application.query.filter_by(reference_number=reference_number).first()
        
        if not application:
            return jsonify({
                'success': False,
                'message': 'Application not found'
            }), 404
        
        return jsonify({
            'success': True,
            'data': application.to_dict()
        })
        
    except Exception as e:
        return jsonify({
            'success': False,
            'message': f'Error fetching application: {str(e)}'
        }), 500

@application_bp.route('/applications/track', methods=['POST'])
def track_application():
    """Track application status by reference number or NID"""
    try:
        data = request.get_json()
        reference_number = data.get('reference_number')
        nid_number = data.get('nid_number')
        
        if not reference_number and not nid_number:
            return jsonify({
                'success': False,
                'message': 'Either reference number or NID number is required'
            }), 400
        
        query = Application.query
        if reference_number:
            query = query.filter_by(reference_number=reference_number)
        elif nid_number:
            query = query.filter_by(nid_number=nid_number)
        
        applications = query.all()
        
        if not applications:
            return jsonify({
                'success': False,
                'message': 'No applications found'
            }), 404
        
        return jsonify({
            'success': True,
            'data': [app.to_dict() for app in applications]
        })
        
    except Exception as e:
        return jsonify({
            'success': False,
            'message': f'Error tracking application: {str(e)}'
        }), 500

@application_bp.route('/applications', methods=['GET'])
def get_applications():
    """Get all applications with pagination and filtering (Admin only)"""
    try:
        page = request.args.get('page', 1, type=int)
        per_page = request.args.get('per_page', 10, type=int)
        status = request.args.get('status')
        district = request.args.get('district')
        division = request.args.get('division')
        category_id = request.args.get('category_id', type=int)
        
        query = Application.query
        
        # Apply filters
        if status:
            query = query.filter_by(status=status)
        if district:
            query = query.filter_by(district=district)
        if division:
            query = query.filter_by(division=division)
        if category_id:
            query = query.filter_by(category_id=category_id)
        
        # Order by creation date (newest first)
        query = query.order_by(Application.created_at.desc())
        
        # Paginate
        pagination = query.paginate(
            page=page, per_page=per_page, error_out=False
        )
        
        return jsonify({
            'success': True,
            'data': [app.to_dict() for app in pagination.items],
            'pagination': {
                'page': page,
                'per_page': per_page,
                'total': pagination.total,
                'pages': pagination.pages,
                'has_next': pagination.has_next,
                'has_prev': pagination.has_prev
            }
        })
        
    except Exception as e:
        return jsonify({
            'success': False,
            'message': f'Error fetching applications: {str(e)}'
        }), 500

@application_bp.route('/applications/<int:application_id>/status', methods=['PUT'])
def update_application_status(application_id):
    """Update application status (Admin only)"""
    try:
        application = Application.query.get_or_404(application_id)
        data = request.get_json()
        
        new_status = data.get('status')
        if new_status not in ['Pending', 'Approved', 'Rejected', 'In Progress']:
            return jsonify({
                'success': False,
                'message': 'Invalid status. Must be one of: Pending, Approved, Rejected, In Progress'
            }), 400
        
        old_status = application.status
        application.status = new_status
        db.session.commit()
        
        # Send status update email
        try:
            if old_status != new_status:
                email_service = EmailService()
                email_service.send_status_update(application, old_status, new_status)
        except Exception as e:
            print(f"Error sending status update email: {str(e)}")
            # Don't fail the status update if email fails
        
        return jsonify({
            'success': True,
            'message': 'Application status updated successfully',
            'data': application.to_dict()
        })
        
    except Exception as e:
        db.session.rollback()
        return jsonify({
            'success': False,
            'message': f'Error updating application status: {str(e)}'
        }), 500

@application_bp.route('/applications/stats', methods=['GET'])
def get_application_stats():
    """Get application statistics (Admin only)"""
    try:
        # Total applications
        total_applications = Application.query.count()
        
        # Applications by status
        status_stats = db.session.query(
            Application.status,
            db.func.count(Application.id)
        ).group_by(Application.status).all()
        
        # Applications by district
        district_stats = db.session.query(
            Application.district,
            db.func.count(Application.id)
        ).group_by(Application.district).all()
        
        # Applications by category
        category_stats = db.session.query(
            Category.name,
            db.func.count(Application.id)
        ).join(Application).group_by(Category.name).all()
        
        # Daily applications (last 30 days)
        from datetime import date, timedelta
        thirty_days_ago = date.today() - timedelta(days=30)
        daily_stats = db.session.query(
            db.func.date(Application.created_at),
            db.func.count(Application.id)
        ).filter(
            Application.created_at >= thirty_days_ago
        ).group_by(
            db.func.date(Application.created_at)
        ).all()
        
        return jsonify({
            'success': True,
            'data': {
                'total_applications': total_applications,
                'status_distribution': dict(status_stats),
                'district_distribution': dict(district_stats),
                'category_distribution': dict(category_stats),
                'daily_applications': {str(date): count for date, count in daily_stats}
            }
        })
        
    except Exception as e:
        return jsonify({
            'success': False,
            'message': f'Error fetching statistics: {str(e)}'
        }), 500

