# Job Portal Project

This is a Django-based job portal application developed as part of MCA coursework. It allows:

- Employers to post jobs, manage listings, and review applicants.
- Job seekers to create profiles, search and save jobs, and submit applications.

## Features

- Custom user roles (employer / seeker)
- Profile management with file uploads (logos, resumes)
- Job search with filters (keyword, category, location, type)
- Job bookmarking for seekers
- Application tracking and status updates
- Email notifications for applications and status changes
- Responsive Bootstrap-based UI

## Technologies

- Python 3.x
- Django 5.2
- SQLite3 (development)
- Bootstrap 5

## Setup

```bash
python -m venv venv
source venv/bin/activate  # or venv\Scripts\activate on Windows
pip install -r requirements.txt
python manage.py migrate
python manage.py runserver
```

## License

This project is licensed under the MIT License. See [LICENSE](LICENSE) for details.


<!-- {% load static %}
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Job Portal</title>

    <link href="https://cdn.jsdelivr.net/npm/bootstrap@5.3.3/dist/css/bootstrap.min.css" rel="stylesheet">
    <link rel="stylesheet" href="{% static 'css/style.css' %}">
</head>
<body class="d-flex flex-column min-vh-100">

<nav class="navbar navbar-expand-lg navbar-dark bg-dark shadow-sm">
    <div class="container">
        <a class="navbar-brand fw-bold" href="{% url 'home' %}">JobPortal</a>

        <button class="navbar-toggler" type="button" data-bs-toggle="collapse" data-bs-target="#navbarContent">
            <span class="navbar-toggler-icon"></span>
        </button>

        <div class="collapse navbar-collapse" id="navbarContent">
            <ul class="navbar-nav ms-auto">

                <li class="nav-item">
                    <a class="nav-link" href="{% url 'home' %}">Home</a>
                </li>

                <li class="nav-item">
                    <a class="nav-link" href="{% url 'job_list' %}">Jobs</a>
                </li>

                {% if user.is_authenticated %}
                    {% if user.role == 'employer' %}
                        <li class="nav-item">
                            <a class="nav-link" href="{% url 'employer_dashboard' %}">Dashboard</a>
                        </li>
                        <li class="nav-item">
                            <a class="nav-link" href="{% url 'employer_profile' %}">Profile</a>
                        </li>
                        <li class="nav-item">
                            <a class="nav-link" href="{% url 'create_job' %}">Post Job</a>
                        </li>
                        <li class="nav-item">
                            <a class="nav-link" href="{% url 'employer_job_list' %}">My Jobs</a>
                        </li>
                        <li class="nav-item">
                            <a class="nav-link" href="{% url 'employer_applications' %}">Applicants</a>
                        </li>
                    {% elif user.role == 'seeker' %}
                        <li class="nav-item">
                            <a class="nav-link" href="{% url 'seeker_profile' %}">My Profile</a>
                        </li>
                        <li class="nav-item">
                            <a class="nav-link" href="{% url 'my_applications' %}">Applications</a>
                        </li>
                        <li class="nav-item">
                            <a class="nav-link" href="{% url 'saved_jobs' %}">Saved Jobs</a>
                        </li>
                    {% endif %}

                    <li class="nav-item">
                        <a class="nav-link text-warning" href="{% url 'logout' %}">Logout</a>
                    </li>
                {% else %}
                    <li class="nav-item">
                        <a class="nav-link" href="{% url 'login' %}">Login</a>
                    </li>

                    <li class="nav-item">
                        <a class="nav-link" href="{% url 'register' %}">Register</a>
                    </li>
                {% endif %}

            </ul>
        </div>
    </div>
</nav>

<main class="flex-grow-1">
    <div class="container mt-4">

        {% if messages %}
            {% for message in messages %}
                <div class="alert alert-{{ message.tags }} alert-dismissible fade show shadow-sm" role="alert">
                    {{ message }}
                    <button type="button" class="btn-close" data-bs-dismiss="alert"></button>
                </div>
            {% endfor %}
        {% endif %}

        {% block content %}
        {% endblock %}
    </div>
</main>

<footer class="bg-dark text-light mt-5 py-4">
    <div class="container text-center">
        <p class="mb-1">JobPortal — Professional Django Portfolio Project</p>
        <small>Built with Django, Bootstrap, SQLite and Python</small>
    </div>
</footer>

<script src="https://cdn.jsdelivr.net/npm/bootstrap@5.3.3/dist/js/bootstrap.bundle.min.js"></script>
</body>
</html> -->


<!-- {% extends "base.html" %}

{% block content %}
<div class="hero-section p-5 mb-5 rounded-4 text-center text-md-start">
    <div class="row align-items-center">
        <div class="col-md-8">
            <h1 class="display-5 fw-bold mb-3">Find Your Dream Job with JobPortal</h1>
            <p class="lead mb-4">
                A modern Django-based job portal where employers can post opportunities
                and job seekers can search, save, and apply with ease.
            </p>

            <a href="{% url 'job_list' %}" class="btn btn-primary btn-lg me-2">Browse Jobs</a>

            {% if not user.is_authenticated %}
                <a href="{% url 'register' %}" class="btn btn-outline-dark btn-lg">Create Account</a>
            {% endif %}
        </div>
    </div>
</div>

<div class="row g-4">
    <div class="col-md-4">
        <div class="card shadow-sm h-100 feature-card">
            <div class="card-body">
                <h4>For Employers</h4>
                <p class="mb-0">Post jobs, manage listings, review applicants, and update application statuses easily.</p>
            </div>
        </div>
    </div>

    <div class="col-md-4">
        <div class="card shadow-sm h-100 feature-card">
            <div class="card-body">
                <h4>For Job Seekers</h4>
                <p class="mb-0">Search jobs, save interesting roles, upload resumes, and track applications in one place.</p>
            </div>
        </div>
    </div>

    <div class="col-md-4">
        <div class="card shadow-sm h-100 feature-card">
            <div class="card-body">
                <h4>Portfolio Quality Project</h4>
                <p class="mb-0">This project demonstrates authentication, CRUD, file uploads, filters, email notifications, and dashboards.</p>
            </div>
        </div>
    </div>
</div>

<div class="mt-5">
    <h2 class="mb-4 text-center">Why This Project Stands Out</h2>
    <div class="row g-4">
        <div class="col-md-3">
            <div class="card shadow-sm h-100 text-center p-3">
                <h5>Custom User Roles</h5>
                <p class="mb-0">Employer and seeker workflows separated properly.</p>
            </div>
        </div>
        <div class="col-md-3">
            <div class="card shadow-sm h-100 text-center p-3">
                <h5>Resume Upload</h5>
                <p class="mb-0">Users can upload resumes and apply directly.</p>
            </div>
        </div>
        <div class="col-md-3">
            <div class="card shadow-sm h-100 text-center p-3">
                <h5>Search & Filters</h5>
                <p class="mb-0">Keyword search and job filtering included.</p>
            </div>
        </div>
        <div class="col-md-3">
            <div class="card shadow-sm h-100 text-center p-3">
                <h5>Email Alerts</h5>
                <p class="mb-0">Application and status update notifications supported.</p>
            </div>
        </div>
    </div>
</div>
{% endblock %} -->



body {
    background-color: #f8f9fa;
}

.navbar-brand {
    font-weight: 700;
    letter-spacing: 0.5px;
}

.card {
    border: none;
    border-radius: 16px;
}

.form-control,
.form-select {
    border-radius: 10px;
}

.hero-section {
    background: linear-gradient(135deg, #ffffff, #e9f2ff);
    box-shadow: 0 10px 25px rgba(0, 0, 0, 0.08);
}

.feature-card {
    transition: transform 0.2s ease;
}

.feature-card:hover {
    transform: translateY(-4px);
}

.dashboard-card h2,
.dashboard-card h4 {
    font-weight: 700;
}

.empty-state-card {
    border: 2px dashed #d0d7de;
    background-color: #ffffff;
}

.btn {
    border-radius: 10px;
}

.pagination .page-link {
    border-radius: 8px;
    margin: 0 4px;
}
.job-card {
    height: 100%;
}

.pagination-wrapper {
    clear: both;
    position: relative;
    z-index: 1;
}

.row.mb-5 {
    margin-bottom: 3rem !important;
}

{% extends "base.html" %}

{% block content %}
<div class="hero-section p-5 mb-5 rounded-4 text-center text-md-start">
    <div class="row align-items-center">
        <div class="col-md-8">
            <h1 class="display-5 fw-bold mb-3">Find Your Dream Job with JobPortal</h1>
            <p class="lead mb-4">
                A modern Django-based job portal where employers can post opportunities
                and job seekers can search, save, and apply with ease.
            </p>

            <a href="{% url 'job_list' %}" class="btn btn-primary btn-lg me-2">Browse Jobs</a>

            {% if not user.is_authenticated %}
                <a href="{% url 'register' %}" class="btn btn-outline-dark btn-lg">Create Account</a>
            {% endif %}
        </div>
    </div>
</div>

<div class="row g-4">
    <div class="col-md-4">
        <div class="card shadow-sm h-100 feature-card">
            <div class="card-body">
                <h4>For Employers</h4>
                <p class="mb-0">Post jobs, manage listings, review applicants, and update application statuses easily.</p>
            </div>
        </div>
    </div>

    <div class="col-md-4">
        <div class="card shadow-sm h-100 feature-card">
            <div class="card-body">
                <h4>For Job Seekers</h4>
                <p class="mb-0">Search jobs, save interesting roles, upload resumes, and track applications in one place.</p>
            </div>
        </div>
    </div>

    <div class="col-md-4">
        <div class="card shadow-sm h-100 feature-card">
            <div class="card-body">
                <h4>Portfolio Quality Project</h4>
                <p class="mb-0">This project demonstrates authentication, CRUD, file uploads, filters, email notifications, and dashboards.</p>
            </div>
        </div>
    </div>
</div>

<div class="mt-5">
    <h2 class="mb-4 text-center">Why This Project Stands Out</h2>
    <div class="row g-4">
        <div class="col-md-3">
            <div class="card shadow-sm h-100 text-center p-3">
                <h5>Custom User Roles</h5>
                <p class="mb-0">Employer and seeker workflows separated properly.</p>
            </div>
        </div>
        <div class="col-md-3">
            <div class="card shadow-sm h-100 text-center p-3">
                <h5>Resume Upload</h5>
                <p class="mb-0">Users can upload resumes and apply directly.</p>
            </div>
        </div>
        <div class="col-md-3">
            <div class="card shadow-sm h-100 text-center p-3">
                <h5>Search & Filters</h5>
                <p class="mb-0">Keyword search and job filtering included.</p>
            </div>
        </div>
        <div class="col-md-3">
            <div class="card shadow-sm h-100 text-center p-3">
                <h5>Email Alerts</h5>
                <p class="mb-0">Application and status update notifications supported.</p>
            </div>
        </div>
    </div>
</div>
{% endblock %}