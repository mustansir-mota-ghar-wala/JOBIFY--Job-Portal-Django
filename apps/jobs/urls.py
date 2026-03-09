from django.urls import path
from . import views

urlpatterns = [
    path('create/', views.create_job, name='create_job'),
    path('my-jobs/', views.employer_job_list, name='employer_job_list'),
    path('saved/', views.saved_jobs, name='saved_jobs'),
    path('save/<int:id>/', views.save_job, name='save_job'),
    path('unsave/<int:id>/', views.unsave_job, name='unsave_job'),
    path('edit/<int:id>/', views.edit_job, name='edit_job'),
    path('delete/<int:id>/', views.delete_job, name='delete_job'),
    path('<int:id>/', views.job_detail, name='job_detail'),
    path('', views.job_list, name='job_list'),
]