from django.core.validators import MinLengthValidator
from django.db import models
from django.contrib.auth.models import User

# Create your models here.
LANG_CHOICES = {
    ('py', 'Python'),
    ('java', 'Java'),
    ('c#', 'C#'),
}


TAG_CHOICES = [
    ('back', 'Backend'),
    ('front', 'Frontend'),
    ('qa', 'Q&A'),
    ('ui', 'Design'),
    ('devops', 'DevOPS'),
]


GRADE_CHOICES = [
    ('junior', 'Junior'),
    ('middle', 'Middle'),
    ('senior', 'Senior'),
]


class Project(models.Model):

    name = models.CharField(max_length=255)
    description = models.TextField(null=True, blank=True)
    language = models.CharField(choices=LANG_CHOICES)

    def __str__(self):
        return f'{self.name}: {self.description}. Language: {self.language}'


class Tag(models.Model):

    name = models.CharField(max_length=255, choices=TAG_CHOICES)
    project = models.ManyToManyField('Project', related_name='tags', blank=True)


class Developer(models.Model):

    name = models.CharField(max_length=255)
    grade = models.CharField(choices=GRADE_CHOICES)
    project = models.ManyToManyField('Project', related_name='developers', blank=True)

STATUS_CHOICES = [
    ("new", "New"),
    ("in_progress", "In Progress"),
    ("done", "Done"),
    ("closed", "Closed"),
    ("blocked", "Blocked"),
    ("panding", "Panding"),
]

PRIORITY_CHOICES = [
    ("low", "Low"),
    ("medium", "Medium"),
    ("high", "High"),
    ("critical", "Critical"),
]

class Task(models.Model):
    name = models.CharField(validators=[MinLengthValidator(10)], unique=True)
    description = models.TextField(null=True, blank=True)
    status = models.CharField(max_length=15, choices=STATUS_CHOICES, default="new")
    priority = models.CharField(max_length=15, choices=PRIORITY_CHOICES)
    project = models.ForeignKey('Project', on_delete=models.CASCADE, related_name='tasks')
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    deleted_at = models.DateTimeField(null=True, blank=True)

    due_date = models.DateTimeField(null=True, blank=True)
    tags = models.ManyToManyField(Tag, related_name='tasks', blank=True)

    # assignee = models.ForeignKey(User, on_delete=models.SET_NULL, related_name='tasks', null=True, blank=True)

    def __str__(self):
        return self.name