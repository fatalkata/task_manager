from django.urls import path
from .views import (
    DashboardView,
    TaskCreateView,
    TaskUpdateView,
    TaskDeleteView,
    ToggleTaskStatusView,
)

urlpatterns = [
    path('dashboard/', DashboardView.as_view(), name='dashboard'),
    path('create/', TaskCreateView.as_view(), name='task-create'),
    path('<int:pk>/edit/', TaskUpdateView.as_view(), name='task-update'),
    path('<int:pk>/delete/', TaskDeleteView.as_view(), name='task-delete'),
    path('<int:pk>/toggle/', ToggleTaskStatusView.as_view(), name='task-toggle-status'),
]
