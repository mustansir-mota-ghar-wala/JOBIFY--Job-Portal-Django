from django.urls import path
from . import views

urlpatterns = [
    path('', views.home, name='home'),
    path('register/', views.register_view, name='register'),
    path('login/', views.login_view, name='login'),
    path('logout/', views.logout_view, name='logout'),

    path('employer/dashboard/', views.employer_dashboard, name='employer_dashboard'),
    path('employer/profile/', views.employer_profile_view, name='employer_profile'),
    path('employer/profile/edit/', views.edit_employer_profile, name='edit_employer_profile'),

    path('seeker/profile/', views.seeker_profile_view, name='seeker_profile'),
    path('seeker/profile/edit/', views.edit_seeker_profile, name='edit_seeker_profile'),
]