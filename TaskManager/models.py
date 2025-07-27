from django.db import models
from django.utils import timezone
from datetime import timedelta


# creating a variable with +1 day
one_day_more = timezone.now() + timedelta(days=1)

# Creating a task status choices
TASK_STATUS_CHOICES = [
    ('new', 'New'),
    ('in_progress', 'In Progress'),
    ('pending', 'Pending'),
    ('blocked', 'Blocked'),
    ('done', 'Done'),
]

# Create your models here.

# creating a model Task
class Task(models.Model):
    # creating some fields
    title = models.CharField(max_length=100, unique=True)
    description = models.TextField(default=None, null=False, blank=False)
    categories = models.ManyToManyField('Category', related_name='tasks')
    status = models.CharField(choices=TASK_STATUS_CHOICES)
    deadline = models.DateTimeField(default=one_day_more)
    created_at = models.DateTimeField(auto_now_add=True)

    # creating a stroke method
    def __str__(self):
        return f'"{self.title}". \n\tStatus: {self.status}\n'

    # creating a Meta class
    class Meta:
        # title_date_unique = ('title', 'date')
        db_table = 'task_manager_task'
        ordering = ['-created_at']
        verbose_name = 'Task'
        verbose_name_plural = 'Tasks'
        constraints = [models.UniqueConstraint(fields=['title', 'created_at'], name='unique_task_title_date')]

    @property
    def short_title(self):
        if len(self.title) <= 10:
            return self.title
        else:
            return f'{self.title[:10]}<...>'


# creating a model SubTask
class SubTask(models.Model):
    # creating some fields
    title = models.CharField(max_length=100, unique=True)
    description = models.TextField(default=None, null=False, blank=False)
    task = models.ForeignKey('Task', related_name='subtasks', on_delete=models.CASCADE)
    status = models.CharField(choices=TASK_STATUS_CHOICES)
    deadline = models.DateTimeField(default=one_day_more)
    created_at = models.DateTimeField(auto_now_add=True)

    # creating a stroke method
    def __str__(self):
        return f'"{self.title}". \n\tStatus: {self.status}\n'

    # creating a Meta class
    class Meta:
        db_table = 'task_manager_subtask'
        ordering = ['-created_at']
        verbose_name = 'Sub Task'
        verbose_name_plural = 'Sub Tasks'
        constraints = [models.UniqueConstraint(fields=['title'], name='unique_task_title')]

    @property
    def short_title(self):
        if len(self.title) <= 10:
            return self.title
        else:
            return f'{self.title[:10]}<...>'


# creating model Category
class Category(models.Model):
    # creating some fields
    name = models.CharField(max_length=50)
    description = models.TextField(default=None, null=True, blank=True)
    objects = models.Manager()

    # creating a stroke method
    def __str__(self):
        return f'{self.name}'

    # creating a Meta class
    class Meta:
        db_table = 'task_manager_category'
        verbose_name = 'Category'
        verbose_name_plural = 'Categories'
        constraints = [models.UniqueConstraint(fields=['name'], name='unique_category_name')]