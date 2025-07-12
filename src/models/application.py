from . import db
from datetime import datetime
import uuid

class Application(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    reference_number = db.Column(db.String(20), unique=True, nullable=False)
    
    # Personal Information
    full_name = db.Column(db.String(100), nullable=False)
    father_name = db.Column(db.String(100), nullable=False)
    mother_name = db.Column(db.String(100), nullable=False)
    nid_number = db.Column(db.String(20), nullable=False)
    date_of_birth = db.Column(db.Date, nullable=False)
    occupation = db.Column(db.String(100), nullable=False)
    
    # Address Information
    village = db.Column(db.String(100), nullable=False)
    upazila = db.Column(db.String(100), nullable=False)
    district = db.Column(db.String(100), nullable=False)
    division = db.Column(db.String(100), nullable=False)
    
    # Family Information
    family_members_count = db.Column(db.Integer, nullable=False)
    monthly_income = db.Column(db.Float, nullable=False)
    main_earner_occupation = db.Column(db.String(100), nullable=False)
    
    # Contact Information
    email = db.Column(db.String(120), nullable=False)
    mobile_number = db.Column(db.String(15), nullable=False)
    
    # Document Paths
    photo_path = db.Column(db.String(255))
    signature_path = db.Column(db.String(255))
    nid_image_path = db.Column(db.String(255))
    other_documents_path = db.Column(db.Text)  # JSON string for multiple documents
    
    # Application Status
    status = db.Column(db.String(20), default='Pending')  # Pending, Approved, Rejected, In Progress
    
    # Foreign Key
    category_id = db.Column(db.Integer, db.ForeignKey('category.id'), nullable=False)
    
    # Timestamps
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    
    def __init__(self, **kwargs):
        super(Application, self).__init__(**kwargs)
        if not self.reference_number:
            self.reference_number = self.generate_reference_number()
    
    def generate_reference_number(self):
        """Generate a unique reference number"""
        timestamp = datetime.now().strftime('%Y%m%d')
        unique_id = str(uuid.uuid4())[:8].upper()
        return f"SBS{timestamp}{unique_id}"

    def __repr__(self):
        return f'<Application {self.reference_number}>'

    def to_dict(self):
        return {
            'id': self.id,
            'reference_number': self.reference_number,
            'full_name': self.full_name,
            'father_name': self.father_name,
            'mother_name': self.mother_name,
            'nid_number': self.nid_number,
            'date_of_birth': self.date_of_birth.isoformat() if self.date_of_birth else None,
            'occupation': self.occupation,
            'village': self.village,
            'upazila': self.upazila,
            'district': self.district,
            'division': self.division,
            'family_members_count': self.family_members_count,
            'monthly_income': self.monthly_income,
            'main_earner_occupation': self.main_earner_occupation,
            'email': self.email,
            'mobile_number': self.mobile_number,
            'photo_path': self.photo_path,
            'signature_path': self.signature_path,
            'nid_image_path': self.nid_image_path,
            'other_documents_path': self.other_documents_path,
            'status': self.status,
            'category_id': self.category_id,
            'category_name': self.category.name if self.category else None,
            'created_at': self.created_at.isoformat() if self.created_at else None,
            'updated_at': self.updated_at.isoformat() if self.updated_at else None
        }

