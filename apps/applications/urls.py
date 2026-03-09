from django.urls import path
from . import views

urlpatterns = [
    path('apply/<int:job_id>/', views.apply_job, name='apply_job'),
    path('my-applications/', views.my_applications, name='my_applications'),
    path('employer-applications/', views.employer_applications, name='employer_applications'),
    path('update-status/<int:id>/', views.update_application_status, name='update_application_status'),
]