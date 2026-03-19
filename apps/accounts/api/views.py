from rest_framework import parsers
from rest_framework.exceptions import PermissionDenied
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView

from apps.accounts.models import Company, EmployerProfile, SeekerProfile

from .serializers import EmployerProfileSerializer, SeekerProfileSerializer


class MyProfileAPIView(APIView):
    permission_classes = [IsAuthenticated]
    parser_classes = [parsers.MultiPartParser, parsers.FormParser, parsers.JSONParser]

    def get_serializer(self):
        if self.request.user.role == 'employer':
            profile, _ = EmployerProfile.objects.get_or_create(
                user=self.request.user,
                defaults={'company_name': self.request.user.username},
            )
            return EmployerProfileSerializer, profile
        if self.request.user.role == 'seeker':
            profile, _ = SeekerProfile.objects.get_or_create(
                user=self.request.user,
                defaults={'full_name': self.request.user.username},
            )
            return SeekerProfileSerializer, profile
        raise PermissionDenied('Unsupported user role.')

    def sync_company(self, profile):
        company, _ = Company.objects.get_or_create(
            created_by=self.request.user,
            defaults={'name': profile.company_name or self.request.user.username},
        )
        company.name = profile.company_name or self.request.user.username
        company.description = profile.company_description
        company.website = profile.website
        company.location = profile.location

        if profile.logo:
            company.logo = profile.logo

        company.save()

    def get(self, request):
        serializer_class, profile = self.get_serializer()
        serializer = serializer_class(profile)
        return Response(serializer.data)

    def patch(self, request):
        serializer_class, profile = self.get_serializer()
        serializer = serializer_class(profile, data=request.data, partial=True)
        serializer.is_valid(raise_exception=True)
        profile = serializer.save()

        if request.user.role == 'employer':
            self.sync_company(profile)

        return Response(serializer.data)
