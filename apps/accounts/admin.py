from django.contrib import admin
from .models import CustomUser,EmployerProfile,SeekerProfile
from django.contrib.auth.admin import UserAdmin
# Register your models here.

class CustomUserAdmin(UserAdmin):
    model = CustomUser
    list_display = ('username', 'email', 'role', 'is_staff', 'is_superuser')
    fieldsets = UserAdmin.fieldsets + (
        ('Role Information', {'fields': ('role',)}),
    )
    add_fieldsets = UserAdmin.add_fieldsets + (
        ('Role Information', {'fields': ('role',)}),
    )

admin.site.register(CustomUser,CustomUserAdmin)
admin.site.register(EmployerProfile)
admin.site.register(SeekerProfile)