from django.contrib import messages
from django.shortcuts import render, redirect
from django.contrib.auth import login, logout
from django.contrib.auth.decorators import login_required

from apps.applications.models import Application
from apps.jobs.models import SavedJob

from .forms import (
    RegisterForm,
    LoginForm,
    EmployerProfileForm,
    SeekerProfileForm
)
from .models import EmployerProfile, SeekerProfile, Company


def home(request):
    return render(request, 'home.html')


def register_view(request):
    if request.method == "POST":
        form = RegisterForm(request.POST)
        if form.is_valid():
            user = form.save()

            if user.role == 'employer':
                EmployerProfile.objects.create(
                    user=user,
                    company_name=user.username
                )
                Company.objects.create(
                    name=user.username,
                    created_by=user
                )

            elif user.role == 'seeker':
                SeekerProfile.objects.create(
                    user=user,
                    full_name=user.username
                )

            messages.success(request, 'Registration successful. You can now log in.')
            return redirect('login')
    else:
        form = RegisterForm()

    context = {'form': form}
    return render(request, 'accounts/register.html', context)


def login_view(request):
    if request.user.is_authenticated:
        if request.user.role == 'employer':
            return redirect('employer_dashboard')
        elif request.user.role == 'seeker':
            return redirect('seeker_dashboard')

    if request.method == 'POST':
        form = LoginForm(request, data=request.POST)
        if form.is_valid():
            user = form.get_user()
            login(request, user)
            messages.success(request, 'Login successful.')

            if user.role == 'employer':
                return redirect('employer_dashboard')
            else:
                return redirect('seeker_dashboard')
        else:
            messages.error(request, 'Invalid username or password.')
    else:
        form = LoginForm()

    context = {'form': form}
    return render(request, 'accounts/login.html', context)


@login_required
def logout_view(request):
    logout(request)
    messages.success(request, 'Logged out successfully.')
    return redirect('login')


@login_required
def employer_dashboard(request):
    if request.user.role != 'employer':
        messages.error(request, 'Access denied.')
        return redirect('home')

    jobs = request.user.posted_jobs.all()
    recent_jobs = jobs.order_by('-created_at')[:5]
    active_jobs_count = jobs.filter(is_active=True).count()
    total_applications = 0
    shortlisted_count = 0

    for job in jobs:
        total_applications += job.applications.count()
        shortlisted_count += job.applications.filter(status='shortlisted').count()

    profile = request.user.employer_profile
    company = request.user.companies.first()

    context = {
        'profile': profile,
        'company': company,
        'total_applications': total_applications,
        'active_jobs_count': active_jobs_count,
        'shortlisted_count': shortlisted_count,
        'recent_jobs': recent_jobs,
    }
    return render(request, 'accounts/employer_dashboard.html', context)


@login_required
def employer_profile_view(request):
    if request.user.role != 'employer':
        messages.error(request, 'Access denied.')
        return redirect('home')

    profile = request.user.employer_profile
    company = request.user.companies.first()

    context = {
        'profile': profile,
        'company': company,
    }
    return render(request, 'accounts/employer_profile.html', context)


@login_required
def seeker_dashboard(request):
    if request.user.role != 'seeker':
        messages.error(request, 'Access denied.')
        return redirect('home')

    profile = request.user.seeker_profile
    applications = Application.objects.filter(applicant=request.user).select_related('job')
    saved_jobs = SavedJob.objects.filter(user=request.user).select_related('job')

    total_applications = applications.count()
    shortlisted_count = applications.filter(status='shortlisted').count()
    reviewed_count = applications.filter(status='reviewed').count()
    rejected_count = applications.filter(status='rejected').count()
    pending_count = applications.filter(status='pending').count()
    saved_jobs_count = saved_jobs.count()

    recent_applications = applications.order_by('-applied_at')[:5]
    recent_saved_jobs = saved_jobs.order_by('-saved_at')[:4]

    completion_items = [
        {
            'label': 'Full name',
            'completed': bool(profile.full_name),
            'hint': 'Add your full professional name.',
        },
        {
            'label': 'Skills',
            'completed': bool(profile.skills),
            'hint': 'Highlight tools, technologies, and strengths.',
        },
        {
            'label': 'Education',
            'completed': bool(profile.education),
            'hint': 'List your degree, college, or certifications.',
        },
        {
            'label': 'Experience',
            'completed': bool(profile.experience),
            'hint': 'Show internships, freelance work, or roles.',
        },
        {
            'label': 'Resume',
            'completed': bool(profile.resume),
            'hint': 'Upload an updated resume to apply faster.',
        },
    ]
    completed_items = sum(1 for item in completion_items if item['completed'])
    profile_completion = completed_items * 20
    response_count = reviewed_count + shortlisted_count + rejected_count
    response_rate = round((response_count / total_applications) * 100) if total_applications else 0

    context = {
        'profile': profile,
        'total_applications': total_applications,
        'shortlisted_count': shortlisted_count,
        'reviewed_count': reviewed_count,
        'rejected_count': rejected_count,
        'pending_count': pending_count,
        'response_count': response_count,
        'response_rate': response_rate,
        'saved_jobs_count': saved_jobs_count,
        'recent_applications': recent_applications,
        'recent_saved_jobs': recent_saved_jobs,
        'profile_completion': profile_completion,
        'completion_items': completion_items,
        'completed_items': completed_items,
    }
    return render(request, 'accounts/seeker_dashboard.html', context)


@login_required
def seeker_profile_view(request):
    if request.user.role != 'seeker':
        messages.error(request, 'Access denied.')
        return redirect('home')

    profile = request.user.seeker_profile
    context = {'profile': profile}
    return render(request, 'accounts/seeker_profile.html', context)


@login_required
def edit_employer_profile(request):
    if request.user.role != 'employer':
        messages.error(request, 'Access denied.')
        return redirect('home')

    profile = request.user.employer_profile
    company = request.user.companies.first()

    if not company:
        company = Company.objects.create(
            name=profile.company_name or request.user.username,
            created_by=request.user
        )

    if request.method == "POST":
        form = EmployerProfileForm(request.POST, request.FILES, instance=profile)
        if form.is_valid():
            profile = form.save()

            company.name = profile.company_name
            company.description = profile.company_description
            company.website = profile.website
            company.location = profile.location

            if profile.logo:
                company.logo = profile.logo

            company.save()

            messages.success(request, 'Employer profile updated successfully.')
            return redirect('employer_profile')
    else:
        form = EmployerProfileForm(instance=profile)

    context = {'form': form}
    return render(request, 'accounts/edit_employer_profile.html', context)


@login_required
def edit_seeker_profile(request):
    if request.user.role != 'seeker':
        messages.error(request, 'Access denied.')
        return redirect('home')

    profile = request.user.seeker_profile

    if request.method == 'POST':
        form = SeekerProfileForm(request.POST, request.FILES, instance=profile)
        if form.is_valid():
            form.save()
            messages.success(request, 'Profile updated successfully.')
            return redirect('seeker_profile')
    else:
        form = SeekerProfileForm(instance=profile)

    context = {'form': form}
    return render(request, 'accounts/edit_seeker_profile.html', context)
