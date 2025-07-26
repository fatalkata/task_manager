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

    FOLDER_CHOICES = [
        ('dz', 'Домашна работа'),
        ('work', 'Работа'),
        ('personal', 'Лични'),
        ('project', 'Проект'),
    ]

    title = models.CharField(max_length=200)
    description = models.TextField()
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='todo')
    due_date = models.DateField(null=True, blank=True)

    assigned_to = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True)

    priority = models.CharField(max_length=10, choices=PRIORITY_CHOICES, default='medium')
    folder = models.CharField(max_length=20, choices=FOLDER_CHOICES, default='personal')



class Comment(models.Model):
    task = models.ForeignKey(Task, on_delete=models.CASCADE, related_name='comments')
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    content = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Comment by {self.user.username}"


class Team(models.Model):
    name = models.CharField(max_length=100)
    members = models.ManyToManyField(User)


    def __str__(self):
        return self.name



