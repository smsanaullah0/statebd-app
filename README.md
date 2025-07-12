# Dost Aid Bangladesh Society - Application Portal

A comprehensive web application for managing project applications with automated PDF generation and email notifications.

## 🌟 Features

### User Features
1. **Application Category Selection** - Dynamic categories managed from admin panel
2. **Multi-step Application Form** - Personal, family, address, and contact information
3. **Document Upload** - Photo, signature, NID, and other documents
4. **Automatic PDF Generation** - Official application letter format
5. **Email Notifications** - Confirmation emails with PDF attachments
6. **Application Tracking** - Track status using reference number
7. **Responsive Design** - Works on desktop and mobile devices

### Admin Features
1. **Secure Admin Login** - Email/password authentication
2. **Category Management** - Add, edit, delete application categories
3. **Application Management** - View, search, filter applications
4. **Status Updates** - Change application status with email notifications
5. **Statistics Dashboard** - Application counts and status distribution
6. **PDF Generation** - Download application PDFs
7. **Search & Filter** - By reference number, NID, status, category

## 🏗️ Technical Architecture

### Backend
- **Framework**: Flask (Python)
- **Database**: SQLite with SQLAlchemy ORM
- **PDF Generation**: ReportLab
- **Email Service**: Flask-Mail (configurable SMTP)
- **File Uploads**: Werkzeug secure file handling
- **API**: RESTful JSON API with CORS support

### Frontend
- **Technology**: Vanilla JavaScript, HTML5, CSS3
- **UI Framework**: Bootstrap 5
- **Icons**: Font Awesome
- **Responsive**: Mobile-first design
- **Features**: Multi-step forms, file upload, real-time validation

### Database Schema
- **Users**: Basic user management
- **Categories**: Dynamic application categories
- **Applications**: Complete application data with file paths
- **Admins**: Admin user management with password hashing

## 📁 Project Structure

```
state_bangladesh_society/
├── src/
│   ├── models/
│   │   ├── __init__.py          # Database initialization
│   │   ├── user.py              # User model
│   │   ├── category.py          # Category model
│   │   ├── application.py       # Application model
│   │   └── admin.py             # Admin model
│   ├── routes/
│   │   ├── user.py              # User routes
│   │   ├── category.py          # Category management
│   │   ├── application.py       # Application handling
│   │   ├── admin.py             # Admin authentication
│   │   └── pdf.py               # PDF generation routes
│   ├── services/
│   │   ├── __init__.py          # Services initialization
│   │   ├── pdf_generator.py     # PDF generation service
│   │   └── email_service.py     # Email service
│   ├── static/
│   │   ├── index.html           # Main application interface
│   │   ├── admin.html           # Admin panel interface
│   │   ├── app.js               # Frontend JavaScript
│   │   └── admin.js             # Admin panel JavaScript
│   └── main.py                  # Flask application entry point
├── uploads/                     # File upload directory
│   ├── photos/                  # User photos
│   ├── signatures/              # User signatures
│   ├── nid_images/              # NID images
│   ├── documents/               # Other documents
│   └── pdfs/                    # Generated PDFs
├── init_db.py                   # Database initialization script
├── requirements.txt             # Python dependencies
└── README.md                    # This file
```

## 🚀 Installation & Setup

### Prerequisites
- Python 3.11+
- pip (Python package manager)

### Installation Steps

1. **Clone/Extract the project**
   ```bash
   cd state_bangladesh_society
   ```

2. **Create virtual environment**
   ```bash
   python -m venv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate
   ```

3. **Install dependencies**
   ```bash
   pip install -r requirements.txt
   ```

4. **Initialize database**
   ```bash
   python init_db.py
   ```

5. **Run the application**
   ```bash
   python src/main.py
   ```

6. **Access the application**
   - Main Application: http://localhost:5000
   - Admin Panel: http://localhost:5000/admin.html

## 🔐 Default Admin Credentials

- **Email**: admin@statebd.org
- **Password**: admin123

**⚠️ Important**: Change the default admin password after first login!

## 📋 API Endpoints

### Categories
- `GET /api/categories` - Get all categories
- `POST /api/categories` - Create new category (Admin)
- `PUT /api/categories/{id}` - Update category (Admin)
- `DELETE /api/categories/{id}` - Delete category (Admin)

### Applications
- `POST /api/applications` - Submit new application
- `GET /api/applications` - Get applications (with pagination)
- `GET /api/applications/{id}` - Get specific application
- `GET /api/applications/track/{reference}` - Track by reference number
- `PUT /api/applications/{id}/status` - Update status (Admin)
- `GET /api/applications/stats` - Get statistics (Admin)

### PDF & Email
- `GET /api/applications/{id}/pdf` - Download application PDF
- `GET /api/applications/{reference}/pdf-by-reference` - Download PDF by reference
- `POST /api/applications/{id}/send-email` - Send confirmation email
- `POST /api/applications/{reference}/send-email-by-reference` - Send email by reference

### Admin
- `POST /api/admin/login` - Admin login
- `POST /api/admin/logout` - Admin logout
- `GET /api/admin/check-auth` - Check authentication
- `POST /api/admin/change-password` - Change password

## 🎨 Customization

### Adding New Categories
1. Login to admin panel
2. Go to Categories section
3. Click "Add Category"
4. Enter name and description
5. Save

### Email Configuration
Edit `src/services/email_service.py` to configure SMTP settings:
```python
self.smtp_server = "your-smtp-server.com"
self.smtp_port = 587
self.username = "your-email@domain.com"
self.password = "your-app-password"
```

### PDF Customization
Modify `src/services/pdf_generator.py` to customize:
- PDF layout and styling
- Header and footer content
- Logo and branding
- Field arrangements

## 🔧 Configuration

### File Upload Settings
- Maximum file size: 16MB
- Supported formats: JPG, PNG, PDF
- Upload directory: `uploads/`

### Database Configuration
- Default: SQLite (`src/database/app.db`)
- Can be changed to PostgreSQL/MySQL by updating `SQLALCHEMY_DATABASE_URI`

### Security Settings
- CORS enabled for all origins (development)
- File upload validation
- SQL injection protection via SQLAlchemy
- Password hashing with Werkzeug

## 📱 Mobile Responsiveness

The application is fully responsive and works on:
- Desktop computers
- Tablets
- Mobile phones
- Different screen orientations

## 🐛 Troubleshooting

### Common Issues

1. **Database not found**
   ```bash
   python init_db.py
   ```

2. **File upload errors**
   - Check upload directory permissions
   - Verify file size limits
   - Ensure supported file formats

3. **PDF generation fails**
   - Check ReportLab installation
   - Verify upload directory exists
   - Check file paths in database

4. **Email not sending**
   - Configure SMTP settings
   - Check email service credentials
   - Verify network connectivity

## 🚀 Deployment

### Production Deployment

1. **Use production WSGI server**
   ```bash
   pip install gunicorn
   gunicorn -w 4 -b 0.0.0.0:5000 src.main:app
   ```

2. **Configure environment variables**
   ```bash
   export FLASK_ENV=production
   export SECRET_KEY=your-secret-key
   export DATABASE_URL=your-database-url
   ```

3. **Set up reverse proxy (Nginx)**
   ```nginx
   server {
       listen 80;
       server_name your-domain.com;
       
       location / {
           proxy_pass http://127.0.0.1:5000;
           proxy_set_header Host $host;
           proxy_set_header X-Real-IP $remote_addr;
       }
   }
   ```

4. **Configure SSL certificate**
   ```bash
   certbot --nginx -d your-domain.com
   ```

### Docker Deployment

Create `Dockerfile`:
```dockerfile
FROM python:3.11-slim

WORKDIR /app
COPY requirements.txt .
RUN pip install -r requirements.txt

COPY . .
RUN python init_db.py

EXPOSE 5000
CMD ["gunicorn", "-w", "4", "-b", "0.0.0.0:5000", "src.main:app"]
```

Build and run:
```bash
docker build -t state-bangladesh-society .
docker run -p 5000:5000 state-bangladesh-society
```

## 📊 Performance Optimization

### Database Optimization
- Add indexes for frequently queried fields
- Use database connection pooling
- Implement query optimization

### File Handling
- Implement file compression
- Use CDN for static files
- Add file caching

### Frontend Optimization
- Minify CSS and JavaScript
- Implement lazy loading
- Use browser caching

## 🔒 Security Considerations

### Production Security
- Change default admin credentials
- Use strong secret keys
- Implement rate limiting
- Add input validation
- Use HTTPS in production
- Regular security updates

### File Upload Security
- Validate file types
- Scan for malware
- Limit file sizes
- Sanitize file names

## 📈 Monitoring & Analytics

### Application Monitoring
- Log application errors
- Monitor response times
- Track user activities
- Database performance

### Business Analytics
- Application submission rates
- Category popularity
- Status distribution
- Geographic analysis

## 🤝 Contributing

1. Fork the repository
2. Create feature branch
3. Make changes
4. Test thoroughly
5. Submit pull request

## 📄 License

This project is licensed under the MIT License - see the LICENSE file for details.

## 📞 Support

For support and questions:
- Email: support@statebd.org
- Documentation: [Project Wiki]
- Issues: [GitHub Issues]

## 🙏 Acknowledgments

- Bootstrap for UI components
- Font Awesome for icons
- ReportLab for PDF generation
- Flask community for excellent documentation

---

**State Bangladesh Society** - Empowering communities through development projects and social initiatives.

