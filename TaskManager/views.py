from django.db.migrations import serializer
from django.db.models import F
from django.db.models.functions import Concat
from django.http import HttpResponse, JsonResponse
from rest_framework.decorators import action
from rest_framework.generics import GenericAPIView, ListCreateAPIView
from rest_framework.pagination import PageNumberPagination
from TaskManager.models import Task, SubTask, Category
from django.utils import timezone
from datetime import timedelta
from rest_framework import generics, status, viewsets
from rest_framework.views import APIView
from rest_framework.response import Response
from .serializers import TaskSerializer, SubTaskSerializer, CategoryCreateSerializer
from django.db.models import Count
from django.db.models.functions import ExtractWeekDay
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import filters


class TaskListCreateView(generics.ListCreateAPIView):
    queryset = Task.objects.all()
    serializer_class = TaskSerializer
    filter_backends = [DjangoFilterBackend, filters.SearchFilter, filters.OrderingFilter]
    filterset_fields = ['status', 'deadline']
    search_fields = ['title', 'description']
    ordering_fields = ['created_at']


    def get(self, request, *args, **kwargs):
        tasks = self.get_queryset()
        serializer = self.get_serializer(tasks, many=True)
        return Response(serializer.data)

    def post(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(serializer.data)

class TasksDetailUpdateDeleteView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Task.objects.all()
    serializer_class = TaskSerializer
    filter_backends = [DjangoFilterBackend, filters.SearchFilter, filters.OrderingFilter]
    filterset_fields = ['status', 'deadline']
    search_fields = ['title', 'description']
    ordering_fields = ['created_at']

    def get(self, requset, *args, **kwargs):
        task = self.get_object()
        serializer = self.get_serializer(task)
        return Response(serializer.data)

    def put(self, request, *args, **kwargs):
        task = self.get_object()
        serializer = self.get_serializer(task, data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(serializer.data)

    def patch(self, request, *args, **kwargs):
        task = self.get_object()
        serializer = self.get_serializer(task, data=request.data, partial=True)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(serializer.data)

    def delete(self, request, *args, **kwargs):
        task = self.get_object()
        task.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)



class SubTaskListCreateView(generics.ListCreateAPIView):
    queryset = SubTask.objects.all()
    serializer_class = SubTaskSerializer
    filter_backends = [DjangoFilterBackend, filters.SearchFilter, filters.OrderingFilter]
    filterset_fields = ['status', 'deadline']
    search_fields = ['title', 'description']
    ordering_fields = ['created_at']

    def get(self, requset, *args, **kwargs):
        subtasks = self.get_queryset()
        serializer = self.get_serializer(subtasks, many=True)
        return Response(serializer.data)

    def post(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(serializer.data)


class SubTaskDetailUpdateDeleteView(generics.RetrieveUpdateDestroyAPIView):
    queryset = SubTask.objects.all()
    serializer_class = SubTaskSerializer
    filter_backends = [DjangoFilterBackend, filters.SearchFilter, filters.OrderingFilter]
    filterset_fields = ['status', 'deadline']
    search_fields = ['title', 'description']
    ordering_fields = ['created_at']

    def get(self, requset, *args, **kwargs):
        subtask = self.get_object()
        serializer = self.get_serializer(subtask)
        return Response(serializer.data)

    def put(self, request, *args, **kwargs):
        subtask = self.get_object()
        serializer = self.get_serializer(subtask, data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(serializer.data)

    def patch(self, request, *args, **kwargs):
        subtask = self.get_object()
        serializer = self.get_serializer(subtask, data=request.data, partial=True)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(serializer.data)

    def delete(self, request, *args, **kwargs):
        subtask = self.get_object()
        subtask.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)


# class SubTaskListView(APIView, PageNumberPagination):
#     page_size = 5
#
#     def get(self, request):
#         subtasks = SubTask.objects.order_by('-created_at')
#         results = self.paginate_queryset(subtasks, request, view=self)
#         serializer = SubTaskSerializer(results, many=True)
#         return self.get_paginated_response(serializer.data)
#
#     def get_page_size(self, request):
#         page_size = request.query_params.get('page_size')
#         if page_size and page_size.isdigit():
#             return int(page_size)
#         return self.page_size


STATUS_CHOICES = {
    'new': 'New',
    'in_progress': 'In Progress',
    'pending': 'Pending',
    'blocked': 'Blocked',
    'done': 'Done'
}


class SubTaskFilteredListView(generics.ListAPIView):
    serializer_class = SubTaskSerializer

    def get_queryset(self):
        queryset = SubTask.objects.select_related('task')

        task_title = self.request.query_params.get('title')
        if task_title:
            queryset = queryset.filter(task__title__icontains=task_title)

        status = self.request.query_params.get('status')
        if status in STATUS_CHOICES:
            queryset = queryset.filter(status=status)

        return queryset


class SubTaskDetailView(generics.RetrieveUpdateDestroyAPIView):
    queryset = SubTask.objects.all()
    serializer_class = SubTaskSerializer


weekdays = {
    'monday': 2,
    'tuesday': 3,
    'wednesday': 4,
    'thursday': 5,
    'friday': 6,
    'saturday': 7,
    'sunday': 1,
}


class TaskByWeekDayView(APIView):
    def get(self, request, *args, **kwargs):
        day_param = request.query_params.get('day', '').strip().lower()

        queryset = Task.objects.annotate(weekday=ExtractWeekDay('created_at'))

        if day_param and day_param in weekdays:
            weekday_number = weekdays[day_param]
            founded_tasks = queryset.filter(weekday=weekday_number)

            if not founded_tasks.exists():
                founded_tasks = queryset

        else:
            founded_tasks = queryset

        serializer = TaskSerializer(founded_tasks, many=True)
        return Response(serializer.data)


class CategoryViewSet(viewsets.ModelViewSet):
    queryset = Category.objects.filter(is_deleted=False)
    serializer_class = CategoryCreateSerializer

    @action(detail=False, methods=['get'])
    def count_tasks(self, request):
        tasks_count = Category.objects.annotate(amount=Count('tasks'))
        data = [
            {
                'id': category.id,
                'category': category.name,
                'task_count': category.amount
            }
            for category in tasks_count
        ]
        return Response(data)


# class TaskCreateView(generics.CreateAPIView):
#     queryset = Task.objects.all()
#     serializer_class = TaskSerializer
#
#
# class TaskListView(generics.ListAPIView):
#     queryset = Task.objects.all()
#     serializer_class = TaskSerializer


# class TaskDetailView(generics.RetrieveAPIView):
#     queryset = Task.objects.all()
#     serializer_class = TaskSerializer
#     lookup_field = 'id'
#
#
# class TaskStatsView(APIView):
#     def get(self, request):
#         total_tasks = Task.objects.count()
#         status_counts = Task.objects.values('status').annotate(count=Count('status'))
#         overdue_tasks = Task.objects.filter(deadline__lt=timezone.now()).count()
#         return Response({
#             'total_tasks': total_tasks,
#             'status_counts': status_counts,
#             'overdue_tasks': overdue_tasks,
#         })


# class SubTaskListCreateView(generics.ListCreateAPIView):
#     queryset = SubTask.objects.all()
#     serializer_class = SubTaskSerializer



# # creating some function to create a task & subtask
# def create_task(response):
#     new_task = Task(title='Prepare presentation',
#                     description='Prepare materials and slides for the presentation',
#                     status='new',
#                     deadline=timezone.now() + timedelta(days=3))
#     new_task.save()
#     return HttpResponse(f'<h1>New task created: "{new_task.title}".</h1> \n<h3>Deadline: {new_task.deadline}</h3>')
#
#
# # do this only if any task was created
# def create_subtask(response):
#     # getting a task "Prepare presentation"
#     get_a_task = Task.objects.get(title='Prepare presentation')
#
#     # creating a subtask 1
#     # new_subtask_1 = SubTask(title='Gather information',
#     #                       description='Find necessary information for the presentation',
#     #                       task=get_a_task,
#     #                       status='new',
#     #                       deadline=timezone.now() + timedelta(days=2))
#     # new_subtask_1.save()
#     # return HttpResponse(f'<h1>New subtask created: "{new_subtask_1.title}".</h1> \n<h3>Deadline: {new_subtask_1.deadline}</h3>')
#
#     # creating subtask 2
#     new_subtask_2 = SubTask(title='Create slides',
#                             description='Create presentation slides',
#                             task=get_a_task,
#                             status='new',
#                             deadline=timezone.now() + timedelta(days=1))
#     new_subtask_2.save()
#     return HttpResponse(f'<h1>New subtask created: "{new_subtask_2.title}".</h1> \n<h3>Deadline: {new_subtask_2.deadline}</h3>')
#
#
# # creating a function to get any task from database
# def read_task(response):
#     # getting all tasks with status "new"
#     all_tasks = Task.objects.filter(status='new')
#
#     # creating a condition for a result of founded tasks
#     if all_tasks.count() > 1:
#         result = '<h3>All founded tasks with status "new":</h3>'
#         for task in all_tasks:
#             result += f'<br>-> "{task.title}"'
#         return HttpResponse(result)
#
#     elif all_tasks.count() == 1:
#         result = '<h3>Only one task was found with status "new":</h3>'
#         for task in all_tasks:
#             result += f'<br>-> "{task.title}"'
#         return HttpResponse(result)
#
#     else:
#         return HttpResponse(f'<h3>Any task was found with status "new"</h3>')
#
#
# # creating a function to get any task from database
# def read_subtask(response):
#     all_subtasks = SubTask.objects.filter(status='done', deadline__lt=timezone.now())
#
#     # creating a condition for a result of founded subtasks
#     if all_subtasks.count() > 1:
#         result = '<h3>All founded tasks with status "done":</h3>'
#         for subtask in all_subtasks:
#             result += f'<br>-> "{subtask.title}"'
#         return HttpResponse(result)
#
#     elif all_subtasks.count() == 1:
#         result = '<h3>Only one task was found with status "done":</h3>'
#         for subtask in all_subtasks:
#             result += f'<br>-> "{subtask.title}"'
#         return HttpResponse(result)
#
#     else:
#         return HttpResponse(f'<h3>Any subtask was found with status "done"</h3>')
#
#
# # creating a function to update a task
# def update_task(response):
#     task = Task.objects.get(title='Prepare presentation')
#
#     # changing some datas
#     task.status = "in_progress"
#
#     # saving changes
#     task.save()
#     return HttpResponse(f'<h3>Task updated: "{task.title}".</h3>')
#
#
# # creating a function to update a subtask
# def update_subtask(response):
#     # first update
#     # subtask = SubTask.objects.get(title='Gather information')
#     # changing some datas
#     # subtask.deadline -= timedelta(days=2)
#
#     # second update
#     subtask = SubTask.objects.get(title='Create slides')
#     # changing some datas
#     subtask.description = 'Create and format presentation slides'
#
#     # saving changes
#     subtask.save()
#     return HttpResponse(f'<h3>Subtask updated: "{subtask.title}".</h3>')
#
#
# def delete_task(response):
#     Task.objects.get(title='Prepare presentation').delete()
#     return HttpResponse(f'<h3>Task was deleted</h3>')