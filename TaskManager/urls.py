from django.urls import path, include
from rest_framework.routers import DefaultRouter
from TaskManager.views import (
    # create_task,
    # create_subtask,
    # read_task,
    # read_subtask,
    # update_task,
    # update_subtask,
    # delete_task,
    # TaskCreateView,
    # TaskListView,
    # TaskDetailView,
    # TaskStatsView,
    # SubTaskListCreateView,
    # SubTaskListView,
    # SubTaskDetailView,
    TaskByWeekDayView,
    SubTaskFilteredListView,

    TaskListCreateView,
    TasksDetailUpdateDeleteView,

    SubTaskListCreateView,
    SubTaskDetailUpdateDeleteView,

    CategoryViewSet, MyTasksView, TaskDetailView,
)

router = DefaultRouter()
router.register(r'categories', CategoryViewSet, basename='category')
# router.register(r'tasks', TaskListCreateView, basename='task')

urlpatterns = [
    # path('create_task', view=create_task),
    # path('create_subtask', view=create_subtask),
    # path('read_task', view=read_task),
    # path('read_subtask', view=read_subtask),
    # path('update_task', view=update_task),
    # path('update_subtask', view=update_subtask),
    # path('delete_task', view=delete_task),
    # path('tasks/create/', TaskCreateView.as_view(), name='task-create'),

    path('tasks/', TaskListCreateView.as_view(), name='task-list'),
    path('tasks/<int:pk>/', TasksDetailUpdateDeleteView.as_view(), name='task-detail'),
    path('tasks/by_weekday/', TaskByWeekDayView.as_view(), name='task-by-weekday'),

    path('mytasks/', MyTasksView.as_view(), name='my-tasks'),
    path('taskdetail/<int:pk>/', TaskDetailView.as_view(), name='task-detail'),

    # path('tasks/stats/', TaskStatsView.as_view(), name='task-stats'),
    # path('subtask/', SubTaskListCreateView.as_view(), name='subtask-list'),

    path('subtasks/', SubTaskListCreateView.as_view(), name='subtask-list'),
    path('subtasks/<int:pk>/', SubTaskDetailUpdateDeleteView.as_view(), name='subtask-detail-update-delete'),
    path('subtasks/filter/', SubTaskFilteredListView.as_view(), name='subtask-filter'),

    path('', include(router.urls)),
]