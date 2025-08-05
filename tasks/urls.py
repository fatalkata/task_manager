from django.urls import path
from .views import (
    # Лични задачи
    DashboardView, TaskCreateView, TaskUpdateView, TaskDeleteView, ToggleTaskStatusView,

    # Екипни задачи
    TeamTasksView, TeamTaskCreateView, TeamTaskUpdateView, TeamTaskDeleteView,

    # Submissions
    SubmitWorkView, SubmissionListView,
)

urlpatterns = [
    # 🗂️ Dashboard & лични задачи
    path('dashboard/', DashboardView.as_view(), name='dashboard'),
    path('create/', TaskCreateView.as_view(), name='task-create'),
    path('<int:pk>/edit/', TaskUpdateView.as_view(), name='task-update'),
    path('<int:pk>/delete/', TaskDeleteView.as_view(), name='task-delete'),
    path('<int:pk>/toggle/', ToggleTaskStatusView.as_view(), name='task-toggle-status'),

    # 👥 Екипни задачи
    path('teams/tasks/', TeamTasksView.as_view(), name='team-tasks'),
    path('teams/<int:team_pk>/create-task/', TeamTaskCreateView.as_view(), name='team-task-create'),
    path('teams/tasks/<int:pk>/edit/', TeamTaskUpdateView.as_view(), name='team-task-edit'),
    path('teams/tasks/<int:pk>/delete/', TeamTaskDeleteView.as_view(), name='team-task-delete'),

    # 📤 Подаване и преглед на задания
    path('teams/tasks/<int:task_pk>/submit/', SubmitWorkView.as_view(), name='submit-work'),
    path('teams/tasks/<int:task_pk>/submissions/', SubmissionListView.as_view(), name='task-submissions'),
]
