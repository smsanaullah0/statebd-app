from flask import Blueprint, request, jsonify, send_file, current_app
import os
from datetime import datetime
from src.models import db, Application
from src.services import PDFGenerator, EmailService

pdf_bp = Blueprint('pdf', __name__)

@pdf_bp.route('/applications/<int:application_id>/pdf', methods=['GET'])
def generate_and_download_pdf(application_id):
    """Generate and download PDF for an application"""
    try:
        # Get application
        application = Application.query.get_or_404(application_id)
        
        # Create PDF generator
        pdf_generator = PDFGenerator(current_app.config['UPLOAD_FOLDER'])
        
        # Generate PDF filename
        timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
        pdf_filename = f"Application_{application.reference_number}_{timestamp}.pdf"
        pdf_path = os.path.join(current_app.config['UPLOAD_FOLDER'], 'pdfs', pdf_filename)
        
        # Ensure PDF directory exists
        os.makedirs(os.path.dirname(pdf_path), exist_ok=True)
        
        # Generate PDF
        success = pdf_generator.generate_application_pdf(application, pdf_path)
        
        if success and os.path.exists(pdf_path):
            return send_file(
                pdf_path,
                as_attachment=True,
                download_name=f"Application_{application.reference_number}.pdf",
                mimetype='application/pdf'
            )
        else:
            return jsonify({
                'success': False,
                'message': 'Error generating PDF'
            }), 500
            
    except Exception as e:
        return jsonify({
            'success': False,
            'message': f'Error generating PDF: {str(e)}'
        }), 500

@pdf_bp.route('/applications/<reference_number>/pdf-by-reference', methods=['GET'])
def generate_pdf_by_reference(reference_number):
    """Generate and download PDF by reference number"""
    try:
        # Get application by reference number
        application = Application.query.filter_by(reference_number=reference_number).first()
        
        if not application:
            return jsonify({
                'success': False,
                'message': 'Application not found'
            }), 404
        
        # Create PDF generator
        pdf_generator = PDFGenerator(current_app.config['UPLOAD_FOLDER'])
        
        # Generate PDF filename
        timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
        pdf_filename = f"Application_{application.reference_number}_{timestamp}.pdf"
        pdf_path = os.path.join(current_app.config['UPLOAD_FOLDER'], 'pdfs', pdf_filename)
        
        # Ensure PDF directory exists
        os.makedirs(os.path.dirname(pdf_path), exist_ok=True)
        
        # Generate PDF
        success = pdf_generator.generate_application_pdf(application, pdf_path)
        
        if success and os.path.exists(pdf_path):
            return send_file(
                pdf_path,
                as_attachment=True,
                download_name=f"Application_{application.reference_number}.pdf",
                mimetype='application/pdf'
            )
        else:
            return jsonify({
                'success': False,
                'message': 'Error generating PDF'
            }), 500
            
    except Exception as e:
        return jsonify({
            'success': False,
            'message': f'Error generating PDF: {str(e)}'
        }), 500

@pdf_bp.route('/applications/<int:application_id>/send-email', methods=['POST'])
def send_application_email(application_id):
    """Send application confirmation email with PDF"""
    try:
        # Get application
        application = Application.query.get_or_404(application_id)
        
        # Create PDF generator and email service
        pdf_generator = PDFGenerator(current_app.config['UPLOAD_FOLDER'])
        email_service = EmailService()
        
        # Generate PDF bytes
        pdf_bytes = pdf_generator.generate_pdf_bytes(application)
        
        if pdf_bytes:
            # Send email with PDF attachment
            success = email_service.send_application_confirmation(application, pdf_bytes)
            
            if success:
                return jsonify({
                    'success': True,
                    'message': 'Email sent successfully'
                })
            else:
                return jsonify({
                    'success': False,
                    'message': 'Error sending email'
                }), 500
        else:
            return jsonify({
                'success': False,
                'message': 'Error generating PDF for email'
            }), 500
            
    except Exception as e:
        return jsonify({
            'success': False,
            'message': f'Error sending email: {str(e)}'
        }), 500

@pdf_bp.route('/applications/<reference_number>/send-email-by-reference', methods=['POST'])
def send_email_by_reference(reference_number):
    """Send application confirmation email by reference number"""
    try:
        # Get application by reference number
        application = Application.query.filter_by(reference_number=reference_number).first()
        
        if not application:
            return jsonify({
                'success': False,
                'message': 'Application not found'
            }), 404
        
        # Create PDF generator and email service
        pdf_generator = PDFGenerator(current_app.config['UPLOAD_FOLDER'])
        email_service = EmailService()
        
        # Generate PDF bytes
        pdf_bytes = pdf_generator.generate_pdf_bytes(application)
        
        if pdf_bytes:
            # Send email with PDF attachment
            success = email_service.send_application_confirmation(application, pdf_bytes)
            
            if success:
                return jsonify({
                    'success': True,
                    'message': 'Email sent successfully'
                })
            else:
                return jsonify({
                    'success': False,
                    'message': 'Error sending email'
                }), 500
        else:
            return jsonify({
                'success': False,
                'message': 'Error generating PDF for email'
            }), 500
            
    except Exception as e:
        return jsonify({
            'success': False,
            'message': f'Error sending email: {str(e)}'
        }), 500

