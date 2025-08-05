from django.shortcuts import get_object_or_404, redirect, render
from django.urls import reverse_lazy
from django.utils import timezone
from datetime import date, timedelta
from django.views.generic import TemplateView, CreateView, UpdateView, DeleteView, ListView, View
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from .models import Task, TeamTask, TeamSubmission, Team
from .forms import TaskForm, TeamTaskForm, SubmissionForm

# 🏠 Dashboard View
class DashboardView(LoginRequiredMixin, TemplateView):
    template_name = 'tasks/dashboard.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        tasks = Task.objects.filter(assigned_to=self.request.user)
        context.update({
            'tasks': tasks,
            'form': TaskForm(),
            'done_tasks': tasks.filter(status='done').count(),
            'total_tasks': tasks.count(),
            'high_priority': tasks.filter(priority='high'),
            'upcoming_tasks': tasks.filter(due_date__gte=date.today(), due_date__lte=date.today() + timedelta(days=7)),
        })
        return context

class TaskCreateView(LoginRequiredMixin, CreateView):
    model = Task
    form_class = TaskForm
    template_name = 'tasks/task_form.html'
    success_url = reverse_lazy('dashboard')

    def form_valid(self, form):
        form.instance.assigned_to = self.request.user
        return super().form_valid(form)

class TaskUpdateView(LoginRequiredMixin, UpdateView):
    model = Task
    form_class = TaskForm
    template_name = 'tasks/task_form.html'
    success_url = reverse_lazy('dashboard')

class TaskDeleteView(LoginRequiredMixin, DeleteView):
    model = Task
    template_name = 'tasks/task_confirm_delete.html'
    success_url = reverse_lazy('dashboard')

class ToggleTaskStatusView(LoginRequiredMixin, View):
    def post(self, request, pk):
        task = get_object_or_404(Task, pk=pk, assigned_to=request.user)
        task.status = 'done' if task.status != 'done' else 'todo'
        task.save()
        return redirect('dashboard')

# 👥 Team Task Views
class TeamTasksView(LoginRequiredMixin, TemplateView):
    template_name = 'tasks/team_tasks.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        user = self.request.user
        leader_teams = Team.objects.filter(leader=user)
        member_teams = Team.objects.filter(members=user).exclude(id__in=leader_teams.values_list('id', flat=True))
        context.update({
            'teams': list(leader_teams) + list(member_teams),
            'today': timezone.now()
        })
        return context

class TeamTaskCreateView(LoginRequiredMixin, UserPassesTestMixin, CreateView):
    model = TeamTask
    form_class = TeamTaskForm
    template_name = 'tasks/team_task_form.html'
    success_url = reverse_lazy('team-tasks')

    def form_valid(self, form):
        team = get_object_or_404(Team, pk=self.kwargs['team_pk'])
        form.instance.team = team
        form.instance.created_by = self.request.user
        return super().form_valid(form)

    def test_func(self):
        team = get_object_or_404(Team, pk=self.kwargs['team_pk'])
        return team.leader == self.request.user

class SubmitWorkView(LoginRequiredMixin, CreateView):
    model = TeamSubmission
    form_class = SubmissionForm
    template_name = 'tasks/submit_work.html'

    def form_valid(self, form):
        task = get_object_or_404(TeamTask, pk=self.kwargs['task_pk'])
        form.instance.task = task
        form.instance.user = self.request.user
        return super().form_valid(form)

    def get_success_url(self):
        return reverse_lazy('team-tasks')

class SubmissionListView(LoginRequiredMixin, UserPassesTestMixin, ListView):
    model = TeamSubmission
    template_name = 'tasks/submissions_list.html'
    context_object_name = 'submissions'

    def get_queryset(self):
        task = get_object_or_404(TeamTask, pk=self.kwargs['task_pk'])
        return TeamSubmission.objects.filter(task=task)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['task'] = get_object_or_404(TeamTask, pk=self.kwargs['task_pk'])
        return context

    def test_func(self):
        task = get_object_or_404(TeamTask, pk=self.kwargs['task_pk'])
        return task.team.leader == self.request.user

class TeamTaskDeleteView(LoginRequiredMixin, UserPassesTestMixin, DeleteView):
    model = TeamTask
    template_name = 'tasks/team_task_confirm_delete.html'
    success_url = reverse_lazy('team-tasks')

    def test_func(self):
        return self.get_object().created_by == self.request.user

class TeamTaskUpdateView(LoginRequiredMixin, UserPassesTestMixin, UpdateView):
    model = TeamTask
    form_class = TeamTaskForm
    template_name = 'tasks/team_task_form.html'
    success_url = reverse_lazy('team-tasks')

    def test_func(self):
        return self.get_object().created_by == self.request.user
