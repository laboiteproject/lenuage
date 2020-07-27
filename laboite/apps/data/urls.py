from django.urls import path
from django.contrib.auth.decorators import login_required

from .views import AppDataCreateView, AppDataUpdateView, AppDataDeleteView


urlpatterns = [
    path("create/", login_required(AppDataCreateView.as_view()), name="create"),
    path("<int:pk>/", login_required(AppDataUpdateView.as_view()), name="update"),
    path("<int:pk>/delete/", login_required(AppDataDeleteView.as_view()), name="delete"),
]
