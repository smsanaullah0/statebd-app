import os
from datetime import datetime
from reportlab.lib.pagesizes import A4
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib.units import inch
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, Image, Table, TableStyle
from reportlab.lib import colors
from reportlab.lib.enums import TA_CENTER, TA_LEFT, TA_RIGHT
from reportlab.pdfgen import canvas
from io import BytesIO
import textwrap

class PDFGenerator:
    def __init__(self, upload_folder):
        self.upload_folder = upload_folder
        self.styles = getSampleStyleSheet()
        self.setup_custom_styles()
    
    def setup_custom_styles(self):
        """Setup custom styles for the PDF"""
        # Title style
        self.title_style = ParagraphStyle(
            'CustomTitle',
            parent=self.styles['Heading1'],
            fontSize=16,
            spaceAfter=30,
            alignment=TA_CENTER,
            textColor=colors.black,
            fontName='Helvetica-Bold'
        )
        
        # Header style
        self.header_style = ParagraphStyle(
            'CustomHeader',
            parent=self.styles['Heading2'],
            fontSize=14,
            spaceAfter=20,
            alignment=TA_CENTER,
            textColor=colors.black,
            fontName='Helvetica-Bold'
        )
        
        # Body style
        self.body_style = ParagraphStyle(
            'CustomBody',
            parent=self.styles['Normal'],
            fontSize=11,
            spaceAfter=12,
            alignment=TA_LEFT,
            textColor=colors.black,
            fontName='Helvetica'
        )
        
        # Bold body style
        self.bold_body_style = ParagraphStyle(
            'CustomBoldBody',
            parent=self.styles['Normal'],
            fontSize=11,
            spaceAfter=12,
            alignment=TA_LEFT,
            textColor=colors.black,
            fontName='Helvetica-Bold'
        )
    
    def generate_application_pdf(self, application, output_path):
        """Generate PDF for application"""
        try:
            # Create the PDF document
            doc = SimpleDocTemplate(
                output_path,
                pagesize=A4,
                rightMargin=72,
                leftMargin=72,
                topMargin=72,
                bottomMargin=72
            )
            
            # Build the story (content)
            story = []
            
            # Add header
            self.add_header(story, application)
            
            # Add photo if available
            self.add_photo(story, application)
            
            # Add application content
            self.add_application_content(story, application)
            
            # Add signature
            self.add_signature(story, application)
            
            # Build the PDF
            doc.build(story)
            
            return True
            
        except Exception as e:
            print(f"Error generating PDF: {str(e)}")
            return False
    
    def add_header(self, story, application):
        """Add header to the PDF"""
        # Title
        title = Paragraph("To,<br/>The Chairman,<br/>State Bangladesh Society", self.title_style)
        story.append(title)
        story.append(Spacer(1, 20))
        
        # Subject
        subject = Paragraph(f"<b>Subject:</b> Application for {application.category.name}", self.header_style)
        story.append(subject)
        story.append(Spacer(1, 20))
        
        # Date and Reference
        date_ref_data = [
            ['Date:', datetime.now().strftime('%B %d, %Y')],
            ['Reference No:', application.reference_number]
        ]
        
        date_ref_table = Table(date_ref_data, colWidths=[1.5*inch, 3*inch])
        date_ref_table.setStyle(TableStyle([
            ('FONTNAME', (0, 0), (-1, -1), 'Helvetica'),
            ('FONTSIZE', (0, 0), (-1, -1), 11),
            ('ALIGN', (0, 0), (0, -1), 'LEFT'),
            ('ALIGN', (1, 0), (1, -1), 'LEFT'),
            ('VALIGN', (0, 0), (-1, -1), 'TOP'),
        ]))
        
        story.append(date_ref_table)
        story.append(Spacer(1, 20))
    
    def add_photo(self, story, application):
        """Add photo to the PDF if available"""
        if application.photo_path:
            try:
                photo_full_path = os.path.join(self.upload_folder, application.photo_path)
                if os.path.exists(photo_full_path):
                    # Create a table to position the photo on the right
                    photo_data = [
                        ['', ''],  # Empty row for spacing
                    ]
                    
                    # Add photo
                    img = Image(photo_full_path, width=1.5*inch, height=2*inch)
                    photo_data.append(['', img])
                    
                    photo_table = Table(photo_data, colWidths=[4.5*inch, 2*inch])
                    photo_table.setStyle(TableStyle([
                        ('ALIGN', (1, 1), (1, 1), 'RIGHT'),
                        ('VALIGN', (1, 1), (1, 1), 'TOP'),
                    ]))
                    
                    story.append(photo_table)
                    story.append(Spacer(1, 10))
            except Exception as e:
                print(f"Error adding photo: {str(e)}")
    
    def add_application_content(self, story, application):
        """Add main application content"""
        # Salutation
        salutation = Paragraph("Respected Sir/Madam,", self.body_style)
        story.append(salutation)
        story.append(Spacer(1, 12))
        
        # Introduction paragraph
        intro_text = f"""I am writing to respectfully submit my application for the {application.category.name} 
        under your esteemed organization. I believe that this project will significantly benefit my family 
        and community, and I am committed to utilizing the assistance effectively."""
        
        intro = Paragraph(intro_text, self.body_style)
        story.append(intro)
        story.append(Spacer(1, 15))
        
        # Personal Information Section
        personal_info_title = Paragraph("<b>Personal Information:</b>", self.bold_body_style)
        story.append(personal_info_title)
        
        personal_data = [
            ['Full Name:', application.full_name],
            ['Father\'s Name:', application.father_name],
            ['Mother\'s Name:', application.mother_name],
            ['National ID Number:', application.nid_number],
            ['Date of Birth:', application.date_of_birth.strftime('%B %d, %Y')],
            ['Occupation:', application.occupation],
        ]
        
        personal_table = Table(personal_data, colWidths=[2*inch, 4*inch])
        personal_table.setStyle(TableStyle([
            ('FONTNAME', (0, 0), (-1, -1), 'Helvetica'),
            ('FONTSIZE', (0, 0), (-1, -1), 11),
            ('ALIGN', (0, 0), (0, -1), 'LEFT'),
            ('ALIGN', (1, 0), (1, -1), 'LEFT'),
            ('VALIGN', (0, 0), (-1, -1), 'TOP'),
            ('LEFTPADDING', (0, 0), (-1, -1), 0),
            ('RIGHTPADDING', (0, 0), (-1, -1), 6),
            ('TOPPADDING', (0, 0), (-1, -1), 3),
            ('BOTTOMPADDING', (0, 0), (-1, -1), 3),
        ]))
        
        story.append(personal_table)
        story.append(Spacer(1, 15))
        
        # Address Information Section
        address_info_title = Paragraph("<b>Address Information:</b>", self.bold_body_style)
        story.append(address_info_title)
        
        address_data = [
            ['Village:', application.village],
            ['Sub-district (Upazila):', application.upazila],
            ['District:', application.district],
            ['Division:', application.division],
        ]
        
        address_table = Table(address_data, colWidths=[2*inch, 4*inch])
        address_table.setStyle(TableStyle([
            ('FONTNAME', (0, 0), (-1, -1), 'Helvetica'),
            ('FONTSIZE', (0, 0), (-1, -1), 11),
            ('ALIGN', (0, 0), (0, -1), 'LEFT'),
            ('ALIGN', (1, 0), (1, -1), 'LEFT'),
            ('VALIGN', (0, 0), (-1, -1), 'TOP'),
            ('LEFTPADDING', (0, 0), (-1, -1), 0),
            ('RIGHTPADDING', (0, 0), (-1, -1), 6),
            ('TOPPADDING', (0, 0), (-1, -1), 3),
            ('BOTTOMPADDING', (0, 0), (-1, -1), 3),
        ]))
        
        story.append(address_table)
        story.append(Spacer(1, 15))
        
        # Family Information Section
        family_info_title = Paragraph("<b>Family Information:</b>", self.bold_body_style)
        story.append(family_info_title)
        
        family_data = [
            ['Number of Family Members:', str(application.family_members_count)],
            ['Monthly Family Income:', f'BDT {application.monthly_income:,.2f}'],
            ['Main Earning Member\'s Occupation:', application.main_earner_occupation],
        ]
        
        family_table = Table(family_data, colWidths=[2.5*inch, 3.5*inch])
        family_table.setStyle(TableStyle([
            ('FONTNAME', (0, 0), (-1, -1), 'Helvetica'),
            ('FONTSIZE', (0, 0), (-1, -1), 11),
            ('ALIGN', (0, 0), (0, -1), 'LEFT'),
            ('ALIGN', (1, 0), (1, -1), 'LEFT'),
            ('VALIGN', (0, 0), (-1, -1), 'TOP'),
            ('LEFTPADDING', (0, 0), (-1, -1), 0),
            ('RIGHTPADDING', (0, 0), (-1, -1), 6),
            ('TOPPADDING', (0, 0), (-1, -1), 3),
            ('BOTTOMPADDING', (0, 0), (-1, -1), 3),
        ]))
        
        story.append(family_table)
        story.append(Spacer(1, 15))
        
        # Contact Information Section
        contact_info_title = Paragraph("<b>Contact Information:</b>", self.bold_body_style)
        story.append(contact_info_title)
        
        contact_data = [
            ['Email Address:', application.email],
            ['Mobile Number:', application.mobile_number],
        ]
        
        contact_table = Table(contact_data, colWidths=[2*inch, 4*inch])
        contact_table.setStyle(TableStyle([
            ('FONTNAME', (0, 0), (-1, -1), 'Helvetica'),
            ('FONTSIZE', (0, 0), (-1, -1), 11),
            ('ALIGN', (0, 0), (0, -1), 'LEFT'),
            ('ALIGN', (1, 0), (1, -1), 'LEFT'),
            ('VALIGN', (0, 0), (-1, -1), 'TOP'),
            ('LEFTPADDING', (0, 0), (-1, -1), 0),
            ('RIGHTPADDING', (0, 0), (-1, -1), 6),
            ('TOPPADDING', (0, 0), (-1, -1), 3),
            ('BOTTOMPADDING', (0, 0), (-1, -1), 3),
        ]))
        
        story.append(contact_table)
        story.append(Spacer(1, 20))
        
        # Closing paragraph
        closing_text = """I humbly request you to consider my application favorably and approve my request 
        for the above-mentioned project. I assure you that I will utilize the assistance properly and 
        follow all the guidelines provided by your organization. I am ready to provide any additional 
        information or documentation if required."""
        
        closing = Paragraph(closing_text, self.body_style)
        story.append(closing)
        story.append(Spacer(1, 15))
        
        # Thank you
        thank_you = Paragraph("Thank you for your kind consideration.", self.body_style)
        story.append(thank_you)
        story.append(Spacer(1, 30))
    
    def add_signature(self, story, application):
        """Add signature section"""
        # Signature section
        signature_data = [
            ['Yours sincerely,', ''],
            ['', ''],
            ['', ''],
        ]
        
        # Add signature image if available
        if application.signature_path:
            try:
                signature_full_path = os.path.join(self.upload_folder, application.signature_path)
                if os.path.exists(signature_full_path):
                    sig_img = Image(signature_full_path, width=2*inch, height=1*inch)
                    signature_data[1] = [sig_img, '']
            except Exception as e:
                print(f"Error adding signature: {str(e)}")
        
        # Add name
        signature_data.append([application.full_name, ''])
        signature_data.append([f'Reference: {application.reference_number}', ''])
        
        signature_table = Table(signature_data, colWidths=[3*inch, 3*inch])
        signature_table.setStyle(TableStyle([
            ('FONTNAME', (0, 0), (-1, -1), 'Helvetica'),
            ('FONTSIZE', (0, 0), (-1, -1), 11),
            ('ALIGN', (0, 0), (0, -1), 'LEFT'),
            ('VALIGN', (0, 0), (-1, -1), 'TOP'),
            ('LEFTPADDING', (0, 0), (-1, -1), 0),
            ('RIGHTPADDING', (0, 0), (-1, -1), 6),
            ('TOPPADDING', (0, 0), (-1, -1), 3),
            ('BOTTOMPADDING', (0, 0), (-1, -1), 3),
        ]))
        
        story.append(signature_table)
    
    def generate_pdf_bytes(self, application):
        """Generate PDF as bytes for email attachment"""
        try:
            buffer = BytesIO()
            doc = SimpleDocTemplate(
                buffer,
                pagesize=A4,
                rightMargin=72,
                leftMargin=72,
                topMargin=72,
                bottomMargin=72
            )
            
            # Build the story (content)
            story = []
            
            # Add header
            self.add_header(story, application)
            
            # Add photo if available
            self.add_photo(story, application)
            
            # Add application content
            self.add_application_content(story, application)
            
            # Add signature
            self.add_signature(story, application)
            
            # Build the PDF
            doc.build(story)
            
            # Get the PDF bytes
            pdf_bytes = buffer.getvalue()
            buffer.close()
            
            return pdf_bytes
            
        except Exception as e:
            print(f"Error generating PDF bytes: {str(e)}")
            return None

