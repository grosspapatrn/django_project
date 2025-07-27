from django.db.models import F
from django.db.models.functions import Concat
from django.http import HttpResponse, JsonResponse
from TaskManager.models import Task, SubTask
from django.utils import timezone
from datetime import timedelta
from rest_framework import generics
from rest_framework.views import APIView
from rest_framework.response import Response
from .serializers import TaskSerializer, SubTaskSerializer
from django.db.models import Count

class TaskCreateView(generics.CreateAPIView):
    queryset = Task.objects.all()
    serializer_class = TaskSerializer


class TaskListView(generics.ListAPIView):
    queryset = Task.objects.all()
    serializer_class = TaskSerializer


class TaskDetailView(generics.RetrieveAPIView):
    queryset = Task.objects.all()
    serializer_class = TaskSerializer
    lookup_field = 'id'


class TaskStatsView(APIView):
    def get(self, request):
        total_tasks = Task.objects.count()
        status_counts = Task.objects.values('status').annotate(count=Count('status'))
        overdue_tasks = Task.objects.filter(deadline__lt=timezone.now()).count()
        return Response({
            'total_tasks': total_tasks,
            'status_counts': status_counts,
            'overdue_tasks': overdue_tasks,
        })


class SubTaskListCreateView(generics.ListCreateAPIView):
    queryset = SubTask.objects.all()
    serializer_class = SubTaskSerializer


class SubTaskDetailView(generics.RetrieveUpdateDestroyAPIView):
    queryset = SubTask.objects.all()
    serializer_class = SubTaskSerializer




# creating some function to create a task & subtask
def create_task(response):
    new_task = Task(title='Prepare presentation',
                    description='Prepare materials and slides for the presentation',
                    status='new',
                    deadline=timezone.now() + timedelta(days=3))
    new_task.save()
    return HttpResponse(f'<h1>New task created: "{new_task.title}".</h1> \n<h3>Deadline: {new_task.deadline}</h3>')


# do this only if any task was created
def create_subtask(response):
    # getting a task "Prepare presentation"
    get_a_task = Task.objects.get(title='Prepare presentation')

    # creating a subtask 1
    # new_subtask_1 = SubTask(title='Gather information',
    #                       description='Find necessary information for the presentation',
    #                       task=get_a_task,
    #                       status='new',
    #                       deadline=timezone.now() + timedelta(days=2))
    # new_subtask_1.save()
    # return HttpResponse(f'<h1>New subtask created: "{new_subtask_1.title}".</h1> \n<h3>Deadline: {new_subtask_1.deadline}</h3>')

    # creating subtask 2
    new_subtask_2 = SubTask(title='Create slides',
                            description='Create presentation slides',
                            task=get_a_task,
                            status='new',
                            deadline=timezone.now() + timedelta(days=1))
    new_subtask_2.save()
    return HttpResponse(f'<h1>New subtask created: "{new_subtask_2.title}".</h1> \n<h3>Deadline: {new_subtask_2.deadline}</h3>')


# creating a function to get any task from database
def read_task(response):
    # getting all tasks with status "new"
    all_tasks = Task.objects.filter(status='new')

    # creating a condition for a result of founded tasks
    if all_tasks.count() > 1:
        result = '<h3>All founded tasks with status "new":</h3>'
        for task in all_tasks:
            result += f'<br>-> "{task.title}"'
        return HttpResponse(result)

    elif all_tasks.count() == 1:
        result = '<h3>Only one task was found with status "new":</h3>'
        for task in all_tasks:
            result += f'<br>-> "{task.title}"'
        return HttpResponse(result)

    else:
        return HttpResponse(f'<h3>Any task was found with status "new"</h3>')


# creating a function to get any task from database
def read_subtask(response):
    all_subtasks = SubTask.objects.filter(status='done', deadline__lt=timezone.now())

    # creating a condition for a result of founded subtasks
    if all_subtasks.count() > 1:
        result = '<h3>All founded tasks with status "done":</h3>'
        for subtask in all_subtasks:
            result += f'<br>-> "{subtask.title}"'
        return HttpResponse(result)

    elif all_subtasks.count() == 1:
        result = '<h3>Only one task was found with status "done":</h3>'
        for subtask in all_subtasks:
            result += f'<br>-> "{subtask.title}"'
        return HttpResponse(result)

    else:
        return HttpResponse(f'<h3>Any subtask was found with status "done"</h3>')


# creating a function to update a task
def update_task(response):
    task = Task.objects.get(title='Prepare presentation')

    # changing some datas
    task.status = "in_progress"

    # saving changes
    task.save()
    return HttpResponse(f'<h3>Task updated: "{task.title}".</h3>')


# creating a function to update a subtask
def update_subtask(response):
    # first update
    # subtask = SubTask.objects.get(title='Gather information')
    # changing some datas
    # subtask.deadline -= timedelta(days=2)

    # second update
    subtask = SubTask.objects.get(title='Create slides')
    # changing some datas
    subtask.description = 'Create and format presentation slides'

    # saving changes
    subtask.save()
    return HttpResponse(f'<h3>Subtask updated: "{subtask.title}".</h3>')


def delete_task(response):
    Task.objects.get(title='Prepare presentation').delete()
    return HttpResponse(f'<h3>Task was deleted</h3>')