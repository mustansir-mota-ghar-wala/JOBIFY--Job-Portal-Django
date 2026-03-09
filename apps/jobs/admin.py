from django.contrib import admin
from .models import Category, Job, SavedJob


@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ('id', 'name')


@admin.register(Job)
class JobAdmin(admin.ModelAdmin):
    list_display = ('id', 'title', 'employer', 'category', 'job_type', 'location', 'is_active', 'created_at')
    list_filter = ('job_type', 'is_active', 'category')
    search_fields = ('title', 'location', 'description')


@admin.register(SavedJob)
class SavedJobAdmin(admin.ModelAdmin):
    list_display = ('id', 'user', 'job', 'saved_at')
    search_fields = ('user__username', 'job__title')