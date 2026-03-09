from django.contrib import messages

from django.shortcuts import render, redirect
from django.contrib.auth import login,logout
from django.contrib.auth.decorators import login_required
# Create your views here.
from django.shortcuts import render
from .forms import(
    RegisterForm,
    LoginForm,
    EmployerProfileForm,
    SeekerProfileForm
)
from .models import EmployerProfile,SeekerProfile

def home(request):
    return render(request, 'home.html')

def register_view(request):
    if request.method == "POST":
        form = RegisterForm(request.POST)
        if form.is_valid():
            user = form.save()
            if user.role == 'employer':
                EmployerProfile.objects.create(
                    user = user,
                    company_name = user.username
                )
            elif user.role == 'seeker':
                SeekerProfile.objects.create(
                    user = user,
                    full_name = user.username
                )
            messages.success(request,'Registration successful. You can now log in.')
            return redirect('login')
    else:
        form = RegisterForm()
    context = {'form':form}
    return render(request,'accounts/register.html',context)
    
def login_view(request):
    if request.user.is_authenticated:
        if request.user.role == 'employer':
            return redirect('employer_dashboard')
        elif request.user.role == 'seeker':
            return redirect('seeker_profile')
        
    if request.method == 'POST':
        form = LoginForm(request,data=request.POST)
        if form.is_valid():
            user = form.get_user()
            login(request,user)
            messages.success(request,'Login successful.')
            if user.role == 'employer':
                return redirect('employer_dashboard')
            else:
                return redirect('seeker_profile')
        else:
            messages.error(request, 'Invalid username or password.')
    else:
        form = LoginForm()
    context = {'form':form}
    return render(request,'accounts/login.html',context)
            
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

    total_applications = 0
    for job in request.user.posted_jobs.all():
        total_applications += job.applications.count()

    context = {
        'profile': request.user.employer_profile,
        'total_applications': total_applications,
    }
    return render(request, 'accounts/employer_dashboard.html', context)

@login_required
def employer_profile_view(request):
    if request.user.role != 'employer':
        messages.error(request, 'Access denied.')
        return redirect('home')

    profile = request.user.employer_profile
    context = {'profile': profile}
    return render(request, 'accounts/employer_profile.html', context)

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
        messages.error(request,'Access denied.')
        return redirect('home')
    profile = request.user.employer_profile
    if request.method == "POST":
        form = EmployerProfileForm(request.POST,request.FILES,instance=profile)
        if form.is_valid():
            form.save()
            messages.success(request, 'Employer profile updated successfully.')
            return redirect('employer_profile')
    else:
        form = EmployerProfileForm(instance=profile)
    context = {'form':form}
    return render(request,'accounts/edit_employer_profile.html',context)

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