from django.db import models
from django.contrib.auth.models import User
# Create your models here.


class Task(models.Model):
    STATUS_CHOICES = [
        ('todo', 'To Do'),
        ('in_progress', 'In Progress'),
        ('done', 'Done'),
    ]

    PRIORITY_CHOICES = [
        ('low', 'Low'),
        ('medium', 'Medium'),
        ('high', 'High'),
    ]


    tag = models.CharField(max_length=100, blank=True, null=True)

    title = models.CharField(max_length=200)
    description = models.TextField()
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='todo')
    due_date = models.DateField(null=True, blank=True)

    assigned_to = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True)

    priority = models.CharField(max_length=10, choices=PRIORITY_CHOICES, default='medium')




class Comment(models.Model):
    task = models.ForeignKey(Task, on_delete=models.CASCADE, related_name='comments')
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    content = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Comment by {self.user.username}"


class Team(models.Model):
    name = models.CharField(max_length=100)
    members = models.ManyToManyField(User, related_name='teams')
    leader = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, related_name='led_teams')



    def __str__(self):
        return self.name

class TeamTask(models.Model):
        STATUS_CHOICES = [
            ('todo', 'To Do'),
            ('done', 'Done'),
        ]

        title = models.CharField(max_length=255)
        description = models.TextField()
        due_date = models.DateTimeField()
        team = models.ForeignKey(Team, on_delete=models.CASCADE, related_name='tasks')
        created_by = models.ForeignKey(User, on_delete=models.CASCADE)
        status = models.CharField(max_length=10, choices=STATUS_CHOICES, default='todo')
        def __str__(self):
            return f"{self.title} ({self.team.name})"

class TeamSubmission(models.Model):
    task = models.ForeignKey(TeamTask, on_delete=models.CASCADE, related_name='submissions')
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    submitted_at = models.DateTimeField(auto_now_add=True)
    content = models.TextField(blank=True)
    file = models.FileField(upload_to='submissions/', blank=True, null=True)

    def is_late(self):
        return self.submitted_at > self.task.due_date

    def __str__(self):
        return f"{self.user.username} -> {self.task.title}"