# Quick Setup Guide - State Bangladesh Society

## 🚀 Quick Start (5 minutes)

### Step 1: Prerequisites
Make sure you have Python 3.11+ installed:
```bash
python --version
```

### Step 2: Setup Virtual Environment
```bash
cd state_bangladesh_society
python -m venv venv

# On Windows:
venv\Scripts\activate

# On Mac/Linux:
source venv/bin/activate
```

### Step 3: Install Dependencies
```bash
pip install -r requirements.txt
```

### Step 4: Initialize Database
```bash
python init_db.py
```

### Step 5: Run Application
```bash
python src/main.py
```

### Step 6: Access Application
- **Main Application**: http://localhost:5000
- **Admin Panel**: http://localhost:5000/admin.html

## 🔐 Default Admin Login
- **Email**: admin@statebd.org
- **Password**: admin123

**⚠️ Change this password immediately after first login!**

## ✅ Test the Application

### Test User Flow:
1. Go to http://localhost:5000
2. Click "Start Your Application"
3. Select a category (e.g., Housing Project)
4. Fill out the multi-step form
5. Upload test files (optional)
6. Submit application
7. Note the reference number
8. Download the generated PDF

### Test Admin Flow:
1. Go to http://localhost:5000/admin.html
2. Login with default credentials
3. View dashboard statistics
4. Check recent applications
5. Update application status
6. Generate PDF for any application
7. Manage categories

## 🎯 Key Features Implemented

✅ **User Features**
- Dynamic category selection
- Multi-step application form
- File upload (photo, signature, NID, documents)
- Automatic PDF generation
- Email notifications with PDF attachment
- Application tracking by reference number
- Responsive mobile design

✅ **Admin Features**
- Secure login system
- Dashboard with statistics
- Application management (view, search, filter)
- Status updates with email notifications
- Category management (add, edit, delete)
- PDF generation and download
- Pagination and search functionality

✅ **Technical Features**
- RESTful API with JSON responses
- SQLite database with SQLAlchemy ORM
- Professional PDF generation with ReportLab
- Email service with HTML templates
- File upload handling with security
- CORS support for API access
- Responsive Bootstrap UI

## 📁 Project Structure Overview

```
state_bangladesh_society/
├── src/                     # Source code
│   ├── models/             # Database models
│   ├── routes/             # API endpoints
│   ├── services/           # Business logic (PDF, Email)
│   ├── static/             # Frontend files
│   └── main.py             # Application entry point
├── uploads/                # File storage
├── init_db.py             # Database setup
├── requirements.txt       # Dependencies
├── README.md              # Full documentation
└── SETUP_GUIDE.md         # This file
```

## 🔧 Customization

### Change Organization Name
Edit these files:
- `src/static/index.html` - Update page titles and headers
- `src/static/admin.html` - Update admin panel branding
- `src/services/pdf_generator.py` - Update PDF header text
- `src/services/email_service.py` - Update email templates

### Add New Categories
1. Login to admin panel
2. Go to Categories section
3. Click "Add Category"
4. Categories appear automatically on homepage

### Configure Email (Production)
Edit `src/services/email_service.py`:
```python
self.smtp_server = "smtp.gmail.com"  # Your SMTP server
self.smtp_port = 587
self.username = "your-email@domain.com"
self.password = "your-app-password"
```

## 🚀 Production Deployment

### Option 1: Simple Deployment
```bash
pip install gunicorn
gunicorn -w 4 -b 0.0.0.0:5000 src.main:app
```

### Option 2: Docker Deployment
```bash
# Create Dockerfile (provided in README.md)
docker build -t state-bangladesh-society .
docker run -p 5000:5000 state-bangladesh-society
```

### Option 3: Cloud Deployment
- Upload to cloud platform (Heroku, DigitalOcean, AWS)
- Configure environment variables
- Set up domain and SSL

## 🐛 Troubleshooting

### Common Issues:

**"Module not found" error**
```bash
pip install -r requirements.txt
```

**Database error**
```bash
python init_db.py
```

**Port already in use**
```bash
# Kill existing process
pkill -f "python src/main.py"
# Or use different port
python src/main.py --port 5001
```

**File upload not working**
- Check `uploads/` directory exists
- Verify file permissions
- Check file size (max 16MB)

## 📞 Support

If you encounter any issues:
1. Check the full README.md for detailed documentation
2. Verify all dependencies are installed
3. Ensure Python 3.11+ is being used
4. Check that all required directories exist

## 🎉 You're Ready!

Your State Bangladesh Society application portal is now ready to use. The system includes everything needed for a professional application management system with PDF generation and email notifications.

**Happy coding! 🚀**

