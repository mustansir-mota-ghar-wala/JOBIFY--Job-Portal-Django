from django.urls import path

from .views import MyProfileAPIView

urlpatterns = [
    path('profile/', MyProfileAPIView.as_view(), name='api_my_profile'),
]
