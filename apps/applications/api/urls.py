from django.urls import path

from .views import (
    ApplyJobAPIView,
    EmployerApplicationsAPIView,
    MyApplicationsAPIView,
    UpdateApplicationStatusAPIView,
)

urlpatterns = [
    path('jobs/<int:id>/apply/', ApplyJobAPIView.as_view(), name='api_apply_job'),
    path('applications/me/', MyApplicationsAPIView.as_view(), name='api_my_applications'),
    path('applications/employer/', EmployerApplicationsAPIView.as_view(), name='api_employer_applications'),
    path('applications/<int:id>/status/', UpdateApplicationStatusAPIView.as_view(), name='api_update_application_status'),
]
