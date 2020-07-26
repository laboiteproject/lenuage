from django.urls import path
from django.contrib.auth.decorators import login_required

from .views import AppLuftdatenCreateView, AppLuftdatenUpdateView, AppLuftdatenDeleteView


urlpatterns = [
    path("create/", login_required(AppLuftdatenCreateView.as_view()), name="create"),
    path("<int:pk>/", login_required(AppLuftdatenUpdateView.as_view()), name="update"),
    path("<int:pk>/delete/", login_required(AppLuftdatenDeleteView.as_view()), name="delete"),
]
