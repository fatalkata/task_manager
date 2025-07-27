from django.views.generic import TemplateView, CreateView, UpdateView, DeleteView, View
from django.urls import reverse_lazy
from django.shortcuts import get_object_or_404, redirect
from django.contrib.auth.mixins import LoginRequiredMixin
from .models import Task
from .forms import TaskForm
from datetime import date, timedelta
from django.views.generic import ListView, CreateView, DetailView
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from .models import TeamTask, TeamSubmission, Team
from .forms import TeamTaskForm, SubmissionForm
from django.utils import timezone
from django.views.generic import TemplateView
from django.contrib.auth.mixins import LoginRequiredMixin
from django.utils import timezone
from django.db.models import Q
from .models import Team, TeamTask

class DashboardView(LoginRequiredMixin, TemplateView):
    template_name = 'tasks/dashboard.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        user_tasks = Task.objects.filter(assigned_to=self.request.user)
        context['tasks'] = user_tasks
        context['form'] = TaskForm()
        context['done_tasks'] = user_tasks.filter(status='done').count()
        context['total_tasks'] = user_tasks.count()
        context['high_priority'] = user_tasks.filter(priority='high')
        context['upcoming_tasks'] = user_tasks.filter(due_date__gte=date.today(), due_date__lte=date.today() + timedelta(days=7))
        return context

class TaskCreateView(LoginRequiredMixin, CreateView):
    model = Task
    form_class = TaskForm
    template_name = 'tasks/task_form.html'
    success_url = reverse_lazy('dashboard')

    def form_valid(self, form):
        form.instance.assigned_to = self.request.user
        return super().form_valid(form)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['tasks'] = Task.objects.filter(assigned_to=self.request.user)
        return context

class TaskUpdateView(LoginRequiredMixin, UpdateView):
    model = Task
    form_class = TaskForm
    template_name = 'tasks/task_form.html'
    success_url = reverse_lazy('dashboard')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['tasks'] = Task.objects.filter(assigned_to=self.request.user)
        return context

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



from datetime import datetime

class TeamTasksView(LoginRequiredMixin, TemplateView):
    template_name = 'tasks/team_tasks.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        user = self.request.user

        # Вземаме истински Team обекти, не values_list
        teams_as_leader = Team.objects.filter(leader=user)
        teams_as_member = Team.objects.filter(members=user).exclude(id__in=teams_as_leader.values_list('id', flat=True))

        teams = list(teams_as_leader) + list(teams_as_member)

        context['teams'] = teams
        context['today'] = timezone.now()
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