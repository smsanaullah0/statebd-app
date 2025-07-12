// Global variables
let selectedCategory = null;
let currentStep = 1;
let submittedApplicationId = null;

// API Base URL
const API_BASE_URL = '/api';

// Initialize the application
document.addEventListener('DOMContentLoaded', function() {
    loadCategories();
    setupFileUploadHandlers();
    setupFormValidation();
});

// Load categories from API
async function loadCategories() {
    try {
        const response = await fetch(`${API_BASE_URL}/categories`);
        const result = await response.json();
        
        if (result.success) {
            displayCategories(result.data);
        } else {
            showAlert('Error loading categories: ' + result.message, 'danger');
        }
    } catch (error) {
        console.error('Error loading categories:', error);
        showAlert('Error loading categories. Please refresh the page.', 'danger');
    }
}

// Display categories
function displayCategories(categories) {
    const container = document.getElementById('categoriesContainer');
    container.innerHTML = '';
    
    const categoryIcons = {
        'Housing Project': 'fas fa-home',
        'Tube Well Project': 'fas fa-tint',
        'Education Support': 'fas fa-graduation-cap',
        'Healthcare Support': 'fas fa-heartbeat',
        'Agricultural Support': 'fas fa-seedling',
        'Small Business Support': 'fas fa-store'
    };
    
    categories.forEach(category => {
        const iconClass = categoryIcons[category.name] || 'fas fa-folder';
        
        const categoryCard = document.createElement('div');
        categoryCard.className = 'col-md-6 col-lg-4';
        categoryCard.innerHTML = `
            <div class="category-card" onclick="selectCategory(${category.id}, '${category.name}')">
                <div class="text-center">
                    <i class="${iconClass} category-icon"></i>
                    <h5>${category.name}</h5>
                    <p class="text-muted">${category.description}</p>
                </div>
            </div>
        `;
        container.appendChild(categoryCard);
    });
}

// Select category
function selectCategory(categoryId, categoryName) {
    selectedCategory = { id: categoryId, name: categoryName };
    
    // Remove previous selection
    document.querySelectorAll('.category-card').forEach(card => {
        card.classList.remove('selected');
    });
    
    // Add selection to clicked card
    event.currentTarget.classList.add('selected');
    
    // Show continue button
    setTimeout(() => {
        showApplicationForm();
    }, 500);
}

// Show application form
function showApplicationForm() {
    if (!selectedCategory) {
        showAlert('Please select a category first.', 'warning');
        return;
    }
    
    document.getElementById('categorySelection').style.display = 'none';
    document.getElementById('applicationForm').style.display = 'block';
    
    // Add category to form
    const categoryInput = document.createElement('input');
    categoryInput.type = 'hidden';
    categoryInput.name = 'category_id';
    categoryInput.value = selectedCategory.id;
    document.getElementById('applicationFormData').appendChild(categoryInput);
    
    // Scroll to form
    document.getElementById('applicationForm').scrollIntoView({ behavior: 'smooth' });
}

// Navigation functions
function nextStep(step) {
    if (validateCurrentStep()) {
        // Hide current step
        document.getElementById(getStepElementId(currentStep)).style.display = 'none';
        
        // Update step indicator
        document.getElementById(`step${currentStep}`).classList.remove('active');
        document.getElementById(`step${currentStep}`).classList.add('completed');
        
        // Show next step
        currentStep = step;
        document.getElementById(getStepElementId(currentStep)).style.display = 'block';
        document.getElementById(`step${currentStep}`).classList.add('active');
        
        // Scroll to current step
        document.getElementById(getStepElementId(currentStep)).scrollIntoView({ behavior: 'smooth' });
    }
}

function prevStep(step) {
    // Hide current step
    document.getElementById(getStepElementId(currentStep)).style.display = 'none';
    
    // Update step indicator
    document.getElementById(`step${currentStep}`).classList.remove('active');
    
    // Show previous step
    currentStep = step;
    document.getElementById(getStepElementId(currentStep)).style.display = 'block';
    document.getElementById(`step${currentStep}`).classList.add('active');
    document.getElementById(`step${currentStep}`).classList.remove('completed');
    
    // Scroll to current step
    document.getElementById(getStepElementId(currentStep)).scrollIntoView({ behavior: 'smooth' });
}

function getStepElementId(step) {
    const stepElements = ['personalInfo', 'addressInfo', 'familyInfo', 'documentUpload'];
    return stepElements[step - 1];
}

// Form validation
function validateCurrentStep() {
    const currentStepElement = document.getElementById(getStepElementId(currentStep));
    const requiredFields = currentStepElement.querySelectorAll('[required]');
    let isValid = true;
    
    requiredFields.forEach(field => {
        if (!field.value.trim()) {
            field.classList.add('is-invalid');
            isValid = false;
        } else {
            field.classList.remove('is-invalid');
        }
    });
    
    if (!isValid) {
        showAlert('Please fill in all required fields.', 'warning');
    }
    
    return isValid;
}

// Setup form validation
function setupFormValidation() {
    const form = document.getElementById('applicationFormData');
    
    form.addEventListener('submit', async function(e) {
        e.preventDefault();
        
        if (!validateCurrentStep()) {
            return;
        }
        
        await submitApplication();
    });
    
    // Real-time validation
    const inputs = form.querySelectorAll('input, select, textarea');
    inputs.forEach(input => {
        input.addEventListener('blur', function() {
            if (this.hasAttribute('required') && !this.value.trim()) {
                this.classList.add('is-invalid');
            } else {
                this.classList.remove('is-invalid');
            }
        });
        
        input.addEventListener('input', function() {
            if (this.classList.contains('is-invalid') && this.value.trim()) {
                this.classList.remove('is-invalid');
            }
        });
    });
}

// File upload handlers
function setupFileUploadHandlers() {
    const fileInputs = ['photo', 'signature', 'nidImage', 'otherDocs'];
    
    fileInputs.forEach(inputId => {
        const input = document.getElementById(inputId);
        if (input) {
            input.addEventListener('change', function() {
                handleFileUpload(this, inputId);
            });
        }
    });
}

function handleFileUpload(input, inputId) {
    const files = input.files;
    const previewContainer = document.getElementById(inputId + 'Preview');
    
    if (files.length > 0) {
        previewContainer.innerHTML = '';
        
        Array.from(files).forEach((file, index) => {
            const fileInfo = document.createElement('div');
            fileInfo.className = 'alert alert-info mt-2';
            
            if (file.type.startsWith('image/')) {
                const img = document.createElement('img');
                img.src = URL.createObjectURL(file);
                img.style.maxWidth = '100px';
                img.style.maxHeight = '100px';
                img.className = 'me-2';
                fileInfo.appendChild(img);
            }
            
            const fileName = document.createElement('span');
            fileName.textContent = `${file.name} (${formatFileSize(file.size)})`;
            fileInfo.appendChild(fileName);
            
            const removeBtn = document.createElement('button');
            removeBtn.type = 'button';
            removeBtn.className = 'btn btn-sm btn-outline-danger ms-2';
            removeBtn.innerHTML = '<i class="fas fa-times"></i>';
            removeBtn.onclick = () => {
                fileInfo.remove();
                if (inputId !== 'otherDocs') {
                    input.value = '';
                }
            };
            fileInfo.appendChild(removeBtn);
            
            previewContainer.appendChild(fileInfo);
        });
    }
}

function formatFileSize(bytes) {
    if (bytes === 0) return '0 Bytes';
    const k = 1024;
    const sizes = ['Bytes', 'KB', 'MB', 'GB'];
    const i = Math.floor(Math.log(bytes) / Math.log(k));
    return parseFloat((bytes / Math.pow(k, i)).toFixed(2)) + ' ' + sizes[i];
}

// Submit application
async function submitApplication() {
    const form = document.getElementById('applicationFormData');
    const formData = new FormData(form);
    
    // Show loading spinner
    const submitBtn = form.querySelector('button[type="submit"]');
    const spinner = submitBtn.querySelector('.loading-spinner');
    spinner.classList.add('show');
    submitBtn.disabled = true;
    
    try {
        const response = await fetch(`${API_BASE_URL}/applications`, {
            method: 'POST',
            body: formData
        });
        
        const result = await response.json();
        
        if (result.success) {
            submittedApplicationId = result.data.application_id;
            document.getElementById('referenceNumber').textContent = result.data.reference_number;
            
            // Show success modal
            const modal = new bootstrap.Modal(document.getElementById('successModal'));
            modal.show();
            
        } else {
            showAlert('Error submitting application: ' + result.message, 'danger');
        }
    } catch (error) {
        console.error('Error submitting application:', error);
        showAlert('Error submitting application. Please try again.', 'danger');
    } finally {
        // Hide loading spinner
        spinner.classList.remove('show');
        submitBtn.disabled = false;
    }
}

// Track application
async function trackApplication() {
    const referenceNumber = document.getElementById('trackReference').value.trim();
    const nidNumber = document.getElementById('trackNID').value.trim();
    
    if (!referenceNumber && !nidNumber) {
        showAlert('Please enter either reference number or NID number.', 'warning');
        return;
    }
    
    try {
        const response = await fetch(`${API_BASE_URL}/applications/track`, {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json'
            },
            body: JSON.stringify({
                reference_number: referenceNumber || undefined,
                nid_number: nidNumber || undefined
            })
        });
        
        const result = await response.json();
        
        if (result.success) {
            displayTrackingResults(result.data);
        } else {
            showAlert('No applications found with the provided information.', 'info');
            document.getElementById('trackResults').innerHTML = '';
        }
    } catch (error) {
        console.error('Error tracking application:', error);
        showAlert('Error tracking application. Please try again.', 'danger');
    }
}

// Display tracking results
function displayTrackingResults(applications) {
    const container = document.getElementById('trackResults');
    container.innerHTML = '';
    
    applications.forEach(app => {
        const statusColor = getStatusColor(app.status);
        const applicationCard = document.createElement('div');
        applicationCard.className = 'card mb-3';
        applicationCard.innerHTML = `
            <div class="card-body">
                <div class="row">
                    <div class="col-md-8">
                        <h5 class="card-title">${app.full_name}</h5>
                        <p class="card-text">
                            <strong>Reference Number:</strong> ${app.reference_number}<br>
                            <strong>Category:</strong> ${app.category_name}<br>
                            <strong>Submitted:</strong> ${new Date(app.created_at).toLocaleDateString()}
                        </p>
                    </div>
                    <div class="col-md-4 text-end">
                        <span class="badge bg-${statusColor} fs-6">${app.status}</span>
                    </div>
                </div>
            </div>
        `;
        container.appendChild(applicationCard);
    });
}

function getStatusColor(status) {
    const colors = {
        'Pending': 'warning',
        'Approved': 'success',
        'Rejected': 'danger',
        'In Progress': 'info'
    };
    return colors[status] || 'secondary';
}

// Download PDF (now implemented)
function downloadPDF() {
    if (submittedApplicationId) {
        // Create a link to download the PDF
        const downloadUrl = `${API_BASE_URL}/applications/${submittedApplicationId}/pdf`;
        
        // Create a temporary link and click it
        const link = document.createElement('a');
        link.href = downloadUrl;
        link.download = `Application_${document.getElementById('referenceNumber').textContent}.pdf`;
        document.body.appendChild(link);
        link.click();
        document.body.removeChild(link);
        
        showAlert('PDF download started.', 'success');
    } else {
        showAlert('No application ID available for PDF generation.', 'warning');
    }
}

// Reset form
function resetForm() {
    // Hide modal
    const modal = bootstrap.Modal.getInstance(document.getElementById('successModal'));
    modal.hide();
    
    // Reset form
    document.getElementById('applicationFormData').reset();
    
    // Reset steps
    currentStep = 1;
    document.querySelectorAll('.step').forEach(step => {
        step.classList.remove('active', 'completed');
    });
    document.getElementById('step1').classList.add('active');
    
    // Hide form sections
    document.querySelectorAll('.form-section').forEach(section => {
        if (section.id === 'personalInfo') {
            section.style.display = 'block';
        } else {
            section.style.display = 'none';
        }
    });
    
    // Clear file previews
    document.querySelectorAll('[id$="Preview"]').forEach(preview => {
        preview.innerHTML = '';
    });
    
    // Show category selection
    document.getElementById('applicationForm').style.display = 'none';
    document.getElementById('categorySelection').style.display = 'block';
    
    // Reset selected category
    selectedCategory = null;
    document.querySelectorAll('.category-card').forEach(card => {
        card.classList.remove('selected');
    });
    
    // Scroll to top
    window.scrollTo({ top: 0, behavior: 'smooth' });
}

// Show tracking section
function showTrackingSection() {
    document.getElementById('categorySelection').style.display = 'none';
    document.getElementById('applicationForm').style.display = 'none';
    document.getElementById('trackSection').style.display = 'block';
}

// Show alert
function showAlert(message, type = 'info') {
    // Remove existing alerts
    const existingAlerts = document.querySelectorAll('.alert-floating');
    existingAlerts.forEach(alert => alert.remove());
    
    // Create new alert
    const alert = document.createElement('div');
    alert.className = `alert alert-${type} alert-dismissible fade show alert-floating`;
    alert.style.position = 'fixed';
    alert.style.top = '20px';
    alert.style.right = '20px';
    alert.style.zIndex = '9999';
    alert.style.minWidth = '300px';
    alert.innerHTML = `
        ${message}
        <button type="button" class="btn-close" data-bs-dismiss="alert"></button>
    `;
    
    document.body.appendChild(alert);
    
    // Auto remove after 5 seconds
    setTimeout(() => {
        if (alert.parentNode) {
            alert.remove();
        }
    }, 5000);
}

// Navigation menu handlers
document.addEventListener('DOMContentLoaded', function() {
    // Handle navigation clicks
    document.querySelectorAll('.nav-link').forEach(link => {
        link.addEventListener('click', function(e) {
            const href = this.getAttribute('href');
            
            if (href === '#home') {
                e.preventDefault();
                window.scrollTo({ top: 0, behavior: 'smooth' });
            } else if (href === '#apply') {
                e.preventDefault();
                document.getElementById('categorySelection').style.display = 'block';
                document.getElementById('applicationForm').style.display = 'none';
                document.getElementById('trackSection').style.display = 'none';
                document.getElementById('categorySelection').scrollIntoView({ behavior: 'smooth' });
            } else if (href === '#track') {
                e.preventDefault();
                showTrackingSection();
                document.getElementById('trackSection').scrollIntoView({ behavior: 'smooth' });
            }
        });
    });
});

