
from django import forms
from .models import Task, TeamTask, TeamSubmission

class TaskForm(forms.ModelForm):
    def clean_title(self):
        title = self.cleaned_data['title']
        if "<script>" in title.lower():
            raise forms.ValidationError("JavaScript is not allowed in title.")
        return title

    def clean_description(self):
        description = self.cleaned_data['description']
        if "<script>" in description.lower():
            raise forms.ValidationError("JavaScript is not allowed in description.")
        return description

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

class TeamLeaderRequestForm(forms.Form):
    message = forms.CharField(
        label="Мотиви за Team Leader",
        widget=forms.Textarea(attrs={'rows': 5, 'class': 'form-control'})
    )