from django.contrib import admin
from .models import Task, Comment, Team, TeamTask, TeamSubmission
from django.contrib.admin.sites import NotRegistered

# 🧾 Лични задачи
@admin.register(Task)
class TaskAdmin(admin.ModelAdmin):
    list_display = ('title', 'status', 'assigned_to', 'due_date')
    list_filter = ('status', 'priority')
    search_fields = ('title',)

# 💬 Коментари
@admin.register(Comment)
class CommentAdmin(admin.ModelAdmin):
    list_display = ('task', 'user', 'created_at')

# 👥 Ограничен достъп до Екипи
class TeamRestrictedAdmin(admin.ModelAdmin):
    list_display = ('name', 'leader')
    filter_horizontal = ('members',)

    def get_queryset(self, request):
        qs = super().get_queryset(request)
        if request.user.is_superuser:
            return qs
        return qs.filter(leader=request.user)

    def has_change_permission(self, request, obj=None):
        if request.user.is_superuser:
            return True
        return obj is not None and obj.leader == request.user

    def has_delete_permission(self, request, obj=None):
        return request.user.is_superuser

    def has_add_permission(self, request):
        return request.user.is_superuser

# 💡 Безопасно пререгистриране на Team
try:
    admin.site.unregister(Team)
except NotRegistered:
    pass

admin.site.register(Team, TeamRestrictedAdmin)

# 📝 Екипни задачи
@admin.register(TeamTask)
class TeamTaskAdmin(admin.ModelAdmin):
    list_display = ('title', 'team', 'due_date', 'status')
    list_filter = ('team', 'status')

# 📤 Подадени задания
@admin.register(TeamSubmission)
class TeamSubmissionAdmin(admin.ModelAdmin):
    list_display = ('task', 'user', 'submitted_at', 'is_late')
    list_filter = ('task', 'user')
