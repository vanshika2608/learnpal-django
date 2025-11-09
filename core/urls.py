from django.urls import path
from . import views

urlpatterns = [
    path("", views.dashboard, name="dashboard"),
    path("goals/", views.goals_home, name="goals_home"),
    path("edit/<int:goal_id>/", views.edit_goal, name="edit_goal"),
    path("delete/<int:goal_id>/", views.delete_goal, name="delete_goal"),
    path("resources/", views.resources_list, name="resources"),
    path("resources/add/", views.add_resource, name="add_resource"),
]
