from django.urls import path
from django.contrib.auth.decorators import login_required

from .views import AppTasksUpdateView, AppTasksCreateView, AppTasksDeleteView, get_projects_view

app_name = "laboite"

urlpatterns = [
    path("create/", login_required(AppTasksCreateView.as_view()), name="create"),
    path("<int:pk>/", login_required(AppTasksUpdateView.as_view()), name="update"),
    path("<int:pk>/delete/", login_required(AppTasksDeleteView.as_view()), name="delete"),
    path("projects", login_required(get_projects_view), name="get_projects"),
]
