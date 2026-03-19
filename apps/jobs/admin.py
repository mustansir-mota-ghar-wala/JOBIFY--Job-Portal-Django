from django.contrib import admin
from .models import Category, Job, SavedJob


@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ('id', 'name')
    search_fields = ('name',)


@admin.register(Job)
class JobAdmin(admin.ModelAdmin):
    list_display = (
        'id', 'title', 'employer', 'company', 'category', 'status',
        'employment_type', 'work_mode', 'location', 'is_active', 'created_at',
    )
    list_filter = ('status', 'employment_type', 'work_mode', 'job_type', 'is_active', 'category')
    search_fields = ('title', 'location', 'description', 'employer__username', 'company__name')
    autocomplete_fields = ('employer', 'company', 'category')


@admin.register(SavedJob)
class SavedJobAdmin(admin.ModelAdmin):
    list_display = ('id', 'user', 'job', 'saved_at')
    list_filter = ('saved_at',)
    search_fields = ('user__username', 'user__email', 'job__title')
    autocomplete_fields = ('user', 'job')
