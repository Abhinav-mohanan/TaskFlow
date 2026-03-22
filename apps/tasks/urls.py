from django.urls import path
from.views import (DashboardView, TaskCreateView, TaskUpdateView, TaskDeleteView,
                   TaskListView, TaskToggleView)

urlpatterns = [
    path('dashboard/', DashboardView.as_view(), name='dashboard'),
    path('tasks/create/', TaskCreateView.as_view(), name='task_create'),
    path('tasks/<str:pk>/edit/', TaskUpdateView.as_view(), name='task_edit'),
    path('tasks/<str:pk>/delete/', TaskDeleteView.as_view(), name='task_delete'),
    path('tasks/<str:pk>/toggle/', TaskToggleView.as_view(), name='task_toggle'),
    path('tasks/', TaskListView.as_view(), name='task_list'),
    
]