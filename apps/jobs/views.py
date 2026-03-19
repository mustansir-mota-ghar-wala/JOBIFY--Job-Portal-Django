from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.core.paginator import Paginator
from django.db.models import Q
from django.shortcuts import render, redirect, get_object_or_404

from apps.accounts.models import Company
from apps.applications.models import Application
from .forms import JobForm
from .models import Job, Category, SavedJob


def job_list(request):
    jobs = (
        Job.objects
        .filter(is_active=True, status='published')
        .select_related('company', 'category', 'employer')
    )
    categories = Category.objects.all()

    keyword = request.GET.get('keyword', '')
    category_id = request.GET.get('category', '')
    location = request.GET.get('location', '')
    job_type = request.GET.get('job_type', '')

    if keyword:
        jobs = jobs.filter(
            Q(title__icontains=keyword) |
            Q(description__icontains=keyword) |
            Q(location__icontains=keyword)
        )

    if category_id:
        jobs = jobs.filter(category_id=category_id)

    if location:
        jobs = jobs.filter(location__icontains=location)

    if job_type:
        jobs = jobs.filter(job_type=job_type)

    paginator = Paginator(jobs, 6)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)

    context = {
        'jobs': page_obj,
        'page_obj': page_obj,
        'categories': categories,
        'selected_keyword': keyword,
        'selected_category': category_id,
        'selected_location': location,
        'selected_job_type': job_type,
        'job_types': Job.JOB_TYPE_CHOICES,
    }
    return render(request, 'jobs/job_list.html', context)


def job_detail(request, id):
    job = get_object_or_404(
        Job.objects.select_related('company', 'category', 'employer'),
        id=id,
        is_active=True,
        status='published',
    )

    has_applied = False
    is_saved = False

    if request.user.is_authenticated and request.user.role == 'seeker':
        has_applied = Application.objects.filter(job=job, applicant=request.user).exists()
        is_saved = SavedJob.objects.filter(job=job, user=request.user).exists()

    context = {
        'job': job,
        'has_applied': has_applied,
        'is_saved': is_saved,
    }
    return render(request, 'jobs/job_detail.html', context)


@login_required
def create_job(request):
    if request.user.role != 'employer':
        messages.error(request, 'Only employers can post jobs.')
        return redirect('home')

    if request.method == 'POST':
        form = JobForm(request.POST)
        if form.is_valid():
            job = form.save(commit=False)
            job.employer = request.user

            company = request.user.companies.first()
            if not company:
                company = Company.objects.create(
                    name=request.user.username,
                    created_by=request.user
                )

            job.company = company
            job.save()

            messages.success(request, 'Job posted successfully.')
            return redirect('employer_job_list')
    else:
        form = JobForm()

    context = {'form': form}
    return render(request, 'jobs/create_job.html', context)


@login_required
def employer_job_list(request):
    if request.user.role != 'employer':
        messages.error(request, 'Access denied.')
        return redirect('home')

    jobs = Job.objects.filter(employer=request.user).select_related('company', 'category').order_by('-created_at')

    paginator = Paginator(jobs, 6)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)

    context = {
        'jobs': page_obj,
        'page_obj': page_obj,
    }
    return render(request, 'jobs/employer_job_list.html', context)


@login_required
def edit_job(request, id):
    if request.user.role != 'employer':
        messages.error(request, 'Access denied.')
        return redirect('home')

    job = get_object_or_404(
        Job.objects.select_related('company', 'category'),
        id=id,
        employer=request.user
    )

    if request.method == 'POST':
        form = JobForm(request.POST, instance=job)
        if form.is_valid():
            updated_job = form.save(commit=False)

            if not updated_job.company:
                company = request.user.companies.first()
                if not company:
                    company = Company.objects.create(
                        name=request.user.username,
                        created_by=request.user
                    )
                updated_job.company = company

            updated_job.save()
            messages.success(request, 'Job updated successfully.')
            return redirect('employer_job_list')
    else:
        form = JobForm(instance=job)

    context = {'form': form}
    return render(request, 'jobs/create_job.html', context)


@login_required
def delete_job(request, id):
    if request.user.role != 'employer':
        messages.error(request, 'Access denied.')
        return redirect('home')

    job = get_object_or_404(Job, id=id, employer=request.user)

    if request.method == 'POST':
        job.delete()
        messages.success(request, 'Job deleted successfully.')
        return redirect('employer_job_list')

    context = {'job': job}
    return render(request, 'jobs/delete_job.html', context)


@login_required
def save_job(request, id):
    if request.user.role != 'seeker':
        messages.error(request, 'Only job seekers can save jobs.')
        return redirect('job_detail', id=id)

    job = get_object_or_404(Job, id=id, is_active=True)
    saved_job, created = SavedJob.objects.get_or_create(user=request.user, job=job)

    if created:
        messages.success(request, 'Job saved successfully.')
    else:
        messages.info(request, 'Job is already saved.')

    return redirect('job_detail', id=id)


@login_required
def unsave_job(request, id):
    if request.user.role != 'seeker':
        messages.error(request, 'Only job seekers can remove saved jobs.')
        return redirect('job_detail', id=id)

    job = get_object_or_404(Job, id=id, is_active=True)
    saved_job = SavedJob.objects.filter(user=request.user, job=job).first()

    if saved_job:
        saved_job.delete()
        messages.success(request, 'Saved job removed successfully.')
    else:
        messages.info(request, 'This job was not in your saved list.')

    return redirect('job_detail', id=id)


@login_required
def saved_jobs(request):
    if request.user.role != 'seeker':
        messages.error(request, 'Access denied.')
        return redirect('home')

    saved_jobs_qs = SavedJob.objects.filter(user=request.user).select_related('job', 'job__company', 'job__category')

    paginator = Paginator(saved_jobs_qs, 6)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)

    context = {
        'saved_jobs': page_obj,
        'page_obj': page_obj,
    }
    return render(request, 'jobs/saved_jobs.html', context)
