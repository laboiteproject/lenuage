from django.urls import path
from django.contrib.auth.decorators import login_required

from .views import AppBitmapCreateView, AppBitmapUpdateView, AppBitmapDeleteView


urlpatterns = [
    path("create/", login_required(AppBitmapCreateView.as_view()), name="create"),
    path("<int:pk>/", login_required(AppBitmapUpdateView.as_view()), name="update"),
    path("<int:pk>/delete/", login_required(AppBitmapDeleteView.as_view()), name="delete"),
]
