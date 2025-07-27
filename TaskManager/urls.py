from django.urls import path
from TaskManager.views import (
    create_task,
    create_subtask,
    read_task,
    read_subtask,
    update_task,
    update_subtask,
    delete_task,
    TaskCreateView,
    TaskListView,
    TaskDetailView,
    TaskStatsView,
    SubTaskListCreateView,
    SubTaskDetailView,
)

urlpatterns = [
    path('create_task', view=create_task),
    path('create_subtask', view=create_subtask),
    path('read_task', view=read_task),
    path('read_subtask', view=read_subtask),
    path('update_task', view=update_task),
    path('update_subtask', view=update_subtask),
    path('delete_task', view=delete_task),
    path('tasks/create/', TaskCreateView.as_view(), name='task-create'),
    path('tasks/', TaskListView.as_view(), name='task-list'),
    path('tasks/<int:id>/', TaskDetailView.as_view(), name='task-detail'),
    path('tasks/stats/', TaskStatsView.as_view(), name='task-stats'),
    path('subtask/', SubTaskListCreateView.as_view(), name='subtask-list'),
    path('subtask/<int:pk>', SubTaskDetailView.as_view(), name='subtask-detail-update-delete'),
]