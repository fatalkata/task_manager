from django.contrib import admin
from .models import Task, Comment, Team
from .models import Team, TeamTask, TeamSubmission

@admin.register(Task)
class TaskAdmin(admin.ModelAdmin):
    list_display = ('title', 'status', 'assigned_to', 'due_date')
    list_filter = ('status', 'priority')
    search_fields = ('title',)

@admin.register(Comment)
class CommentAdmin(admin.ModelAdmin):
    list_display = ('task', 'user', 'created_at')

@admin.register(Team)
class TeamAdmin(admin.ModelAdmin):
    list_display = ('name', 'leader')
    filter_horizontal = ('members',)

@admin.register(TeamTask)
class TeamTaskAdmin(admin.ModelAdmin):
    list_display = ('title', 'team', 'due_date', 'status')
    list_filter = ('team', 'status')

@admin.register(TeamSubmission)
class TeamSubmissionAdmin(admin.ModelAdmin):
    list_display = ('task', 'user', 'submitted_at', 'is_late')
    list_filter = ('task', 'user')