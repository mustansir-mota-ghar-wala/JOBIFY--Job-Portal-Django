from django.contrib import admin
from django.contrib.auth.admin import UserAdmin

from .models import Company, CustomUser, EmployerProfile, SeekerProfile


@admin.register(CustomUser)
class CustomUserAdmin(UserAdmin):
    model = CustomUser
    list_display = ('username', 'email', 'role', 'is_staff', 'is_active', 'date_joined')
    list_filter = ('role', 'is_staff', 'is_superuser', 'is_active')
    search_fields = ('username', 'email', 'first_name', 'last_name')
    fieldsets = UserAdmin.fieldsets + (
        ('Role Information', {'fields': ('role',)}),
    )
    add_fieldsets = UserAdmin.add_fieldsets + (
        ('Role Information', {'fields': ('role',)}),
    )


@admin.register(Company)
class CompanyAdmin(admin.ModelAdmin):
    list_display = ('name', 'created_by', 'location', 'website', 'created_at')
    list_filter = ('created_at',)
    search_fields = ('name', 'location', 'created_by__username', 'created_by__email')
    autocomplete_fields = ('created_by',)


@admin.register(EmployerProfile)
class EmployerProfileAdmin(admin.ModelAdmin):
    list_display = ('company_name', 'user', 'website', 'location')
    search_fields = ('company_name', 'user__username', 'user__email', 'location')
    autocomplete_fields = ('user',)


@admin.register(SeekerProfile)
class SeekerProfileAdmin(admin.ModelAdmin):
    list_display = ('full_name', 'user', 'education')
    search_fields = ('full_name', 'user__username', 'user__email', 'skills', 'education')
    autocomplete_fields = ('user',)
