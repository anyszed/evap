from django.contrib import admin
from .models import Project, Task


@admin.register(Project)
class ProjectAdmin(admin.ModelAdmin):
    list_display = ('name', 'done', 'due_date', 'created_at')
    list_filter = ('done',)
    search_fields = ('name',)


@admin.register(Task)
class TaskAdmin(admin.ModelAdmin):
    list_display = ('title', 'project', 'priority', 'done', 'due_date', 'created_at')
    list_filter = ('done', 'priority')
    search_fields = ('title',)