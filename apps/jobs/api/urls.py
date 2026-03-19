from django.urls import path
from .views import (
    EmployerJobListAPIView,
    JobCreateAPIView,
    JobDetailAPIView,
    JobListAPIView,
    JobUpdateDeleteAPIView,
    SavedJobListAPIView,
    SaveJobAPIView,
    UnsaveJobAPIView,
)

urlpatterns = [
    path('jobs/', JobListAPIView.as_view(), name='api_job_list'),
    path('jobs/employer/', EmployerJobListAPIView.as_view(), name='api_employer_job_list'),
    path('jobs/create/', JobCreateAPIView.as_view(), name='api_job_create'),
    path('jobs/<int:id>/', JobDetailAPIView.as_view(), name='api_job_detail'),
    path('jobs/<int:id>/manage/', JobUpdateDeleteAPIView.as_view(), name='api_job_manage'),
    path('jobs/saved/', SavedJobListAPIView.as_view(), name='api_saved_job_list'),
    path('jobs/<int:id>/save/', SaveJobAPIView.as_view(), name='api_save_job'),
    path('jobs/<int:id>/unsave/', UnsaveJobAPIView.as_view(), name='api_unsave_job'),
]
