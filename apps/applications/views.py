from django.conf import settings
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.core.mail import send_mail
from django.core.paginator import Paginator
from django.shortcuts import render, redirect, get_object_or_404

from apps.jobs.models import Job
from .forms import ApplicationForm, ApplicationStatusForm
from .models import Application


@login_required
def apply_job(request, job_id):
    if request.user.role != 'seeker':
        messages.error(request, 'Only job seekers can apply for jobs.')
        return redirect('job_detail', id=job_id)

    job = get_object_or_404(
        Job.objects.select_related('employer', 'company', 'category'),
        id=job_id,
        is_active=True
    )

    already_applied = Application.objects.filter(job=job, applicant=request.user).exists()
    if already_applied:
        messages.warning(request, 'You have already applied for this job.')
        return redirect('job_detail', id=job.id)

    if request.method == 'POST':
        form = ApplicationForm(request.POST, request.FILES)
        if form.is_valid():
            application = form.save(commit=False)
            application.job = job
            application.applicant = request.user
            application.save()

            employer_email = job.employer.email
            seeker_email = request.user.email

            if employer_email:
                send_mail(
                    subject=f'New Application for {job.title}',
                    message=(
                        f'A new application has been submitted for your job "{job.title}".\n\n'
                        f'Applicant: {request.user.username}\n'
                        f'Email: {request.user.email}\n'
                        f'Cover Letter:\n{application.cover_letter or "No cover letter provided."}'
                    ),
                    from_email=settings.DEFAULT_FROM_EMAIL,
                    recipient_list=[employer_email],
                    fail_silently=True,
                )

            if seeker_email:
                send_mail(
                    subject=f'Application Submitted for {job.title}',
                    message=(
                        f'Hello {request.user.username},\n\n'
                        f'Your application for "{job.title}" has been submitted successfully.'
                    ),
                    from_email=settings.DEFAULT_FROM_EMAIL,
                    recipient_list=[seeker_email],
                    fail_silently=True,
                )

            messages.success(request, 'Application submitted successfully.')
            return redirect('my_applications')
    else:
        form = ApplicationForm()

    context = {
        'form': form,
        'job': job,
    }
    return render(request, 'applications/apply_job.html', context)


@login_required
def my_applications(request):
    if request.user.role != 'seeker':
        messages.error(request, 'Access denied.')
        return redirect('home')

    applications = (
        Application.objects
        .filter(applicant=request.user)
        .select_related('job', 'job__company', 'job__category')
        .order_by('-applied_at')
    )

    paginator = Paginator(applications, 6)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)

    context = {
        'applications': page_obj,
        'page_obj': page_obj,
    }
    return render(request, 'applications/my_applications.html', context)


@login_required
def employer_applications(request):
    if request.user.role != 'employer':
        messages.error(request, 'Access denied.')
        return redirect('home')

    applications = (
        Application.objects
        .filter(job__employer=request.user)
        .select_related('job', 'job__company', 'applicant')
        .order_by('-applied_at')
    )

    paginator = Paginator(applications, 6)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)

    context = {
        'applications': page_obj,
        'page_obj': page_obj,
    }
    return render(request, 'applications/employer_applications.html', context)


@login_required
def update_application_status(request, id):
    if request.user.role != 'employer':
        messages.error(request, 'Access denied.')
        return redirect('home')

    application = get_object_or_404(
        Application.objects.select_related('job', 'job__company', 'applicant'),
        id=id,
        job__employer=request.user
    )

    if request.method == 'POST':
        form = ApplicationStatusForm(request.POST, instance=application)
        if form.is_valid():
            updated_application = form.save()

            seeker_email = updated_application.applicant.email
            if seeker_email:
                send_mail(
                    subject=f'Application Status Updated for {updated_application.job.title}',
                    message=(
                        f'Hello {updated_application.applicant.username},\n\n'
                        f'Your application status for "{updated_application.job.title}" '
                        f'has been updated to "{updated_application.get_status_display()}".'
                    ),
                    from_email=settings.DEFAULT_FROM_EMAIL,
                    recipient_list=[seeker_email],
                    fail_silently=True,
                )

            messages.success(request, 'Application status updated successfully.')
            return redirect('employer_applications')
    else:
        form = ApplicationStatusForm(instance=application)

    context = {
        'form': form,
        'application': application,
    }
    return render(request, 'applications/update_application_status.html', context)