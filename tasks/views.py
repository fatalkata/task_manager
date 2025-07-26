from django.views.generic import TemplateView, CreateView, UpdateView, DeleteView, View
from django.urls import reverse_lazy
from django.shortcuts import get_object_or_404, redirect
from django.contrib.auth.mixins import LoginRequiredMixin
from .models import Task
from .forms import TaskForm
from datetime import date, timedelta

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


