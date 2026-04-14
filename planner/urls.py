from django.urls import path
from . import views

app_name = "planner"

urlpatterns = [
    path("", views.planner_home, name="planner_home"),
    path("api/task/<int:task_id>/", views.api_task, name="api_task"),
    path("api/project/<int:project_id>/", views.api_project, name="api_project"),
    path("create_task/", views.create_task, name="create_task"),
    path("create_project/", views.create_project, name="create_project"),
    path("update_task_date/<int:task_id>/", views.update_task_date, name="update_task_date"),
    path("update_project_date/<int:project_id>/", views.update_project_date, name="update_project_date"),
    path("close_task/<int:task_id>/", views.close_task, name="close_task"),
    path("close_project/<int:project_id>/", views.close_project, name="close_project"),    
]