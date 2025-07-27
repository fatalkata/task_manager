
from django import forms
from .models import Task, TeamTask, TeamSubmission

class TaskForm(forms.ModelForm):
    due_date = forms.DateField(
        widget=forms.DateInput(attrs={'type': 'date', 'class': 'form-control'})
    )
    tag = forms.CharField(
        required=False,
        label='Tag (optional)',
        widget=forms.TextInput(attrs={'class': 'form-control'})
    )

    class Meta:
        model = Task
        fields = ['title', 'description', 'status', 'due_date', 'priority', 'tag']


class TeamTaskForm(forms.ModelForm):
    due_date = forms.DateTimeField(
        widget=forms.DateTimeInput(attrs={'type': 'datetime-local', 'class': 'form-control'})
    )

    class Meta:
        model = TeamTask
        fields = ['title', 'description', 'due_date']

class SubmissionForm(forms.ModelForm):
    class Meta:
        model = TeamSubmission
        fields = ['content', 'file']
