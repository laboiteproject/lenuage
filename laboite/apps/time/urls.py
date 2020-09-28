from django.urls import path
from django.contrib.auth.decorators import login_required

from .views import AppTimeUpdateView, AppTimeCreateView, AppTimeDeleteView


app_name = "laboite"

urlpatterns = [
    path("create/", login_required(AppTimeCreateView.as_view()), name="create"),
    path("<int:pk>/", login_required(AppTimeUpdateView.as_view()), name="update"),
    path("<int:pk>/delete/", login_required(AppTimeDeleteView.as_view()), name="delete"),
]
