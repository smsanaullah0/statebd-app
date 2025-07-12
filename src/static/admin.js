// Global variables
let currentAdmin = null;
let currentApplicationId = null;
let currentPage = 1;
let totalPages = 1;

// API Base URL
const API_BASE_URL = '/api';

// Initialize admin panel
document.addEventListener('DOMContentLoaded', function() {
    checkAuthentication();
    setupEventListeners();
});

// Check if admin is already authenticated
async function checkAuthentication() {
    try {
        const response = await fetch(`${API_BASE_URL}/admin/check-auth`);
        const result = await response.json();
        
        if (result.success && result.authenticated) {
            currentAdmin = result.data;
            showDashboard();
        } else {
            showLoginScreen();
        }
    } catch (error) {
        console.error('Authentication check failed:', error);
        showLoginScreen();
    }
}

// Setup event listeners
function setupEventListeners() {
    // Login form
    document.getElementById('loginForm').addEventListener('submit', handleLogin);
    
    // Change password form
    document.getElementById('changePasswordForm').addEventListener('submit', handleChangePassword);
    
    // Search input
    document.getElementById('searchInput').addEventListener('keypress', function(e) {
        if (e.key === 'Enter') {
            searchApplications();
        }
    });
}

// Handle login
async function handleLogin(e) {
    e.preventDefault();
    
    const email = document.getElementById('loginEmail').value;
    const password = document.getElementById('loginPassword').value;
    const submitBtn = e.target.querySelector('button[type="submit"]');
    const spinner = submitBtn.querySelector('.loading-spinner');
    
    // Show loading
    spinner.style.display = 'inline-block';
    submitBtn.disabled = true;
    
    try {
        const response = await fetch(`${API_BASE_URL}/admin/login`, {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json'
            },
            body: JSON.stringify({ email, password })
        });
        
        const result = await response.json();
        
        if (result.success) {
            currentAdmin = result.data.admin;
            showDashboard();
        } else {
            showAlert('Login failed: ' + result.message, 'danger');
        }
    } catch (error) {
        console.error('Login error:', error);
        showAlert('Login failed. Please try again.', 'danger');
    } finally {
        // Hide loading
        spinner.style.display = 'none';
        submitBtn.disabled = false;
    }
}

// Show login screen
function showLoginScreen() {
    document.getElementById('loginScreen').style.display = 'flex';
    document.getElementById('adminDashboard').style.display = 'none';
}

// Show dashboard
function showDashboard() {
    document.getElementById('loginScreen').style.display = 'none';
    document.getElementById('adminDashboard').style.display = 'block';
    
    // Set admin name
    document.getElementById('adminName').textContent = currentAdmin.full_name;
    
    // Load dashboard data
    loadDashboardData();
}

// Load dashboard data
async function loadDashboardData() {
    await Promise.all([
        loadStatistics(),
        loadRecentApplications(),
        loadCategories()
    ]);
}

// Load statistics
async function loadStatistics() {
    try {
        const response = await fetch(`${API_BASE_URL}/applications/stats`);
        const result = await response.json();
        
        if (result.success) {
            displayStatistics(result.data);
        }
    } catch (error) {
        console.error('Error loading statistics:', error);
    }
}

// Display statistics
function displayStatistics(stats) {
    const container = document.getElementById('statsContainer');
    container.innerHTML = '';
    
    const statsCards = [
        {
            title: 'Total Applications',
            value: stats.total_applications,
            icon: 'fas fa-file-alt',
            color: 'primary'
        },
        {
            title: 'Pending',
            value: stats.status_distribution.Pending || 0,
            icon: 'fas fa-clock',
            color: 'warning'
        },
        {
            title: 'Approved',
            value: stats.status_distribution.Approved || 0,
            icon: 'fas fa-check-circle',
            color: 'success'
        },
        {
            title: 'In Progress',
            value: stats.status_distribution['In Progress'] || 0,
            icon: 'fas fa-spinner',
            color: 'info'
        }
    ];
    
    statsCards.forEach(stat => {
        const card = document.createElement('div');
        card.className = 'col-md-3';
        card.innerHTML = `
            <div class="stats-card">
                <div class="d-flex justify-content-between align-items-center">
                    <div>
                        <h6 class="text-muted mb-1">${stat.title}</h6>
                        <div class="stats-number">${stat.value}</div>
                    </div>
                    <div>
                        <i class="${stat.icon} fa-2x text-${stat.color}"></i>
                    </div>
                </div>
            </div>
        `;
        container.appendChild(card);
    });
}

// Load recent applications
async function loadRecentApplications() {
    try {
        const response = await fetch(`${API_BASE_URL}/applications?per_page=5`);
        const result = await response.json();
        
        if (result.success) {
            displayRecentApplications(result.data);
        }
    } catch (error) {
        console.error('Error loading recent applications:', error);
    }
}

// Display recent applications
function displayRecentApplications(applications) {
    const tbody = document.getElementById('recentApplicationsTable');
    tbody.innerHTML = '';
    
    applications.forEach(app => {
        const row = document.createElement('tr');
        row.innerHTML = `
            <td>${app.reference_number}</td>
            <td>${app.full_name}</td>
            <td>${app.category_name}</td>
            <td><span class="status-badge status-${app.status.toLowerCase().replace(' ', '-')}">${app.status}</span></td>
            <td>${new Date(app.created_at).toLocaleDateString()}</td>
            <td>
                <button class="btn btn-sm btn-outline-primary" onclick="viewApplication(${app.id})">
                    <i class="fas fa-eye"></i>
                </button>
                <button class="btn btn-sm btn-outline-success" onclick="showStatusModal(${app.id}, '${app.status}')">
                    <i class="fas fa-edit"></i>
                </button>
            </td>
        `;
        tbody.appendChild(row);
    });
}

// Load categories
async function loadCategories() {
    try {
        const response = await fetch(`${API_BASE_URL}/categories`);
        const result = await response.json();
        
        if (result.success) {
            displayCategories(result.data);
            populateCategoryFilter(result.data);
        }
    } catch (error) {
        console.error('Error loading categories:', error);
    }
}

// Display categories
function displayCategories(categories) {
    const tbody = document.getElementById('categoriesTable');
    tbody.innerHTML = '';
    
    categories.forEach(category => {
        const row = document.createElement('tr');
        row.innerHTML = `
            <td>${category.name}</td>
            <td>${category.description || '-'}</td>
            <td>
                <span class="badge ${category.is_active ? 'bg-success' : 'bg-secondary'}">
                    ${category.is_active ? 'Active' : 'Inactive'}
                </span>
            </td>
            <td>${new Date(category.created_at).toLocaleDateString()}</td>
            <td>
                <button class="btn btn-sm btn-outline-primary" onclick="editCategory(${category.id})">
                    <i class="fas fa-edit"></i>
                </button>
                <button class="btn btn-sm btn-outline-danger" onclick="deleteCategory(${category.id})">
                    <i class="fas fa-trash"></i>
                </button>
            </td>
        `;
        tbody.appendChild(row);
    });
}

// Populate category filter
function populateCategoryFilter(categories) {
    const filter = document.getElementById('categoryFilter');
    filter.innerHTML = '<option value="">All Categories</option>';
    
    categories.forEach(category => {
        const option = document.createElement('option');
        option.value = category.id;
        option.textContent = category.name;
        filter.appendChild(option);
    });
}

// Show section
function showSection(sectionName) {
    // Hide all sections
    document.querySelectorAll('[id$="Section"]').forEach(section => {
        section.style.display = 'none';
    });
    
    // Remove active class from all sidebar items
    document.querySelectorAll('.sidebar-item').forEach(item => {
        item.classList.remove('active');
    });
    
    // Show selected section
    document.getElementById(sectionName + 'Section').style.display = 'block';
    
    // Add active class to clicked sidebar item
    event.target.classList.add('active');
    
    // Load section-specific data
    if (sectionName === 'applications') {
        loadApplications();
    } else if (sectionName === 'categories') {
        loadCategories();
    }
}

// Load applications with pagination
async function loadApplications(page = 1) {
    try {
        const status = document.getElementById('statusFilter').value;
        const category = document.getElementById('categoryFilter').value;
        
        let url = `${API_BASE_URL}/applications?page=${page}&per_page=10`;
        if (status) url += `&status=${status}`;
        if (category) url += `&category_id=${category}`;
        
        const response = await fetch(url);
        const result = await response.json();
        
        if (result.success) {
            displayApplications(result.data);
            displayPagination(result.pagination);
        }
    } catch (error) {
        console.error('Error loading applications:', error);
    }
}

// Display applications
function displayApplications(applications) {
    const tbody = document.getElementById('applicationsTable');
    tbody.innerHTML = '';
    
    applications.forEach(app => {
        const row = document.createElement('tr');
        row.innerHTML = `
            <td>${app.reference_number}</td>
            <td>${app.full_name}</td>
            <td>${app.category_name}</td>
            <td>${app.district}</td>
            <td><span class="status-badge status-${app.status.toLowerCase().replace(' ', '-')}">${app.status}</span></td>
            <td>${new Date(app.created_at).toLocaleDateString()}</td>
            <td>
                <button class="btn btn-sm btn-outline-primary" onclick="viewApplication(${app.id})" title="View Details">
                    <i class="fas fa-eye"></i>
                </button>
                <button class="btn btn-sm btn-outline-success" onclick="showStatusModal(${app.id}, '${app.status}')" title="Update Status">
                    <i class="fas fa-edit"></i>
                </button>
                <button class="btn btn-sm btn-outline-info" onclick="generateApplicationPDF(${app.id})" title="Generate PDF">
                    <i class="fas fa-file-pdf"></i>
                </button>
            </td>
        `;
        tbody.appendChild(row);
    });
}

// Display pagination
function displayPagination(pagination) {
    const container = document.getElementById('pagination');
    container.innerHTML = '';
    
    currentPage = pagination.page;
    totalPages = pagination.pages;
    
    // Previous button
    const prevLi = document.createElement('li');
    prevLi.className = `page-item ${pagination.has_prev ? '' : 'disabled'}`;
    prevLi.innerHTML = `
        <a class="page-link" href="#" onclick="loadApplications(${pagination.page - 1})">Previous</a>
    `;
    container.appendChild(prevLi);
    
    // Page numbers
    for (let i = 1; i <= pagination.pages; i++) {
        const li = document.createElement('li');
        li.className = `page-item ${i === pagination.page ? 'active' : ''}`;
        li.innerHTML = `
            <a class="page-link" href="#" onclick="loadApplications(${i})">${i}</a>
        `;
        container.appendChild(li);
    }
    
    // Next button
    const nextLi = document.createElement('li');
    nextLi.className = `page-item ${pagination.has_next ? '' : 'disabled'}`;
    nextLi.innerHTML = `
        <a class="page-link" href="#" onclick="loadApplications(${pagination.page + 1})">Next</a>
    `;
    container.appendChild(nextLi);
}

// Search applications
function searchApplications() {
    loadApplications(1);
}

// View application details
async function viewApplication(applicationId) {
    try {
        currentApplicationId = applicationId; // Set for PDF generation
        
        const response = await fetch(`${API_BASE_URL}/applications/${applicationId}`);
        const result = await response.json();
        
        if (result.success) {
            displayApplicationDetails(result.data);
            const modal = new bootstrap.Modal(document.getElementById('applicationModal'));
            modal.show();
        }
    } catch (error) {
        console.error('Error loading application details:', error);
        showAlert('Error loading application details.', 'danger');
    }
}

// Display application details
function displayApplicationDetails(application) {
    const container = document.getElementById('applicationDetails');
    container.innerHTML = `
        <div class="row">
            <div class="col-md-6">
                <h6>Personal Information</h6>
                <p><strong>Full Name:</strong> ${application.full_name}</p>
                <p><strong>Father's Name:</strong> ${application.father_name}</p>
                <p><strong>Mother's Name:</strong> ${application.mother_name}</p>
                <p><strong>NID Number:</strong> ${application.nid_number}</p>
                <p><strong>Date of Birth:</strong> ${application.date_of_birth}</p>
                <p><strong>Occupation:</strong> ${application.occupation}</p>
            </div>
            <div class="col-md-6">
                <h6>Address Information</h6>
                <p><strong>Village:</strong> ${application.village}</p>
                <p><strong>Upazila:</strong> ${application.upazila}</p>
                <p><strong>District:</strong> ${application.district}</p>
                <p><strong>Division:</strong> ${application.division}</p>
            </div>
            <div class="col-md-6">
                <h6>Family Information</h6>
                <p><strong>Family Members:</strong> ${application.family_members_count}</p>
                <p><strong>Monthly Income:</strong> BDT ${application.monthly_income}</p>
                <p><strong>Main Earner:</strong> ${application.main_earner_occupation}</p>
            </div>
            <div class="col-md-6">
                <h6>Contact Information</h6>
                <p><strong>Email:</strong> ${application.email}</p>
                <p><strong>Mobile:</strong> ${application.mobile_number}</p>
                <p><strong>Category:</strong> ${application.category_name}</p>
                <p><strong>Status:</strong> <span class="status-badge status-${application.status.toLowerCase().replace(' ', '-')}">${application.status}</span></p>
            </div>
        </div>
    `;
}

// Show status update modal
function showStatusModal(applicationId, currentStatus) {
    currentApplicationId = applicationId;
    document.getElementById('newStatus').value = currentStatus;
    
    const modal = new bootstrap.Modal(document.getElementById('statusModal'));
    modal.show();
}

// Update application status
async function updateApplicationStatus() {
    const newStatus = document.getElementById('newStatus').value;
    
    try {
        const response = await fetch(`${API_BASE_URL}/applications/${currentApplicationId}/status`, {
            method: 'PUT',
            headers: {
                'Content-Type': 'application/json'
            },
            body: JSON.stringify({ status: newStatus })
        });
        
        const result = await response.json();
        
        if (result.success) {
            showAlert('Application status updated successfully.', 'success');
            
            // Hide modal
            const modal = bootstrap.Modal.getInstance(document.getElementById('statusModal'));
            modal.hide();
            
            // Reload applications
            loadApplications(currentPage);
            loadRecentApplications();
        } else {
            showAlert('Error updating status: ' + result.message, 'danger');
        }
    } catch (error) {
        console.error('Error updating status:', error);
        showAlert('Error updating application status.', 'danger');
    }
}

// Show add category modal
function showAddCategoryModal() {
    document.getElementById('addCategoryForm').reset();
    const modal = new bootstrap.Modal(document.getElementById('addCategoryModal'));
    modal.show();
}

// Add category
async function addCategory() {
    const name = document.getElementById('categoryName').value;
    const description = document.getElementById('categoryDescription').value;
    
    try {
        const response = await fetch(`${API_BASE_URL}/categories`, {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json'
            },
            body: JSON.stringify({ name, description })
        });
        
        const result = await response.json();
        
        if (result.success) {
            showAlert('Category added successfully.', 'success');
            
            // Hide modal
            const modal = bootstrap.Modal.getInstance(document.getElementById('addCategoryModal'));
            modal.hide();
            
            // Reload categories
            loadCategories();
        } else {
            showAlert('Error adding category: ' + result.message, 'danger');
        }
    } catch (error) {
        console.error('Error adding category:', error);
        showAlert('Error adding category.', 'danger');
    }
}

// Handle change password
async function handleChangePassword(e) {
    e.preventDefault();
    
    const currentPassword = document.getElementById('currentPassword').value;
    const newPassword = document.getElementById('newPassword').value;
    const confirmPassword = document.getElementById('confirmPassword').value;
    
    if (newPassword !== confirmPassword) {
        showAlert('New passwords do not match.', 'warning');
        return;
    }
    
    try {
        const response = await fetch(`${API_BASE_URL}/admin/change-password`, {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json'
            },
            body: JSON.stringify({
                current_password: currentPassword,
                new_password: newPassword
            })
        });
        
        const result = await response.json();
        
        if (result.success) {
            showAlert('Password changed successfully.', 'success');
            document.getElementById('changePasswordForm').reset();
        } else {
            showAlert('Error changing password: ' + result.message, 'danger');
        }
    } catch (error) {
        console.error('Error changing password:', error);
        showAlert('Error changing password.', 'danger');
    }
}

// Generate PDF (now implemented)
function generatePDF() {
    if (currentApplicationId) {
        // Create a link to download the PDF
        const downloadUrl = `${API_BASE_URL}/applications/${currentApplicationId}/pdf`;
        
        // Create a temporary link and click it
        const link = document.createElement('a');
        link.href = downloadUrl;
        link.download = `Application_${currentApplicationId}.pdf`;
        document.body.appendChild(link);
        link.click();
        document.body.removeChild(link);
        
        showAlert('PDF download started.', 'success');
    } else {
        showAlert('No application selected for PDF generation.', 'warning');
    }
}

function generateApplicationPDF(applicationId) {
    // Create a link to download the PDF
    const downloadUrl = `${API_BASE_URL}/applications/${applicationId}/pdf`;
    
    // Create a temporary link and click it
    const link = document.createElement('a');
    link.href = downloadUrl;
    link.download = `Application_${applicationId}.pdf`;
    document.body.appendChild(link);
    link.click();
    document.body.removeChild(link);
    
    showAlert('PDF download started.', 'success');
}

// Edit category (placeholder)
function editCategory(categoryId) {
    showAlert('Category editing will be available soon.', 'info');
}

// Delete category (placeholder)
function deleteCategory(categoryId) {
    if (confirm('Are you sure you want to delete this category?')) {
        showAlert('Category deletion will be available soon.', 'info');
    }
}

// Logout
async function logout() {
    try {
        await fetch(`${API_BASE_URL}/admin/logout`, { method: 'POST' });
    } catch (error) {
        console.error('Logout error:', error);
    } finally {
        currentAdmin = null;
        showLoginScreen();
    }
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

