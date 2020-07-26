from django.urls import path
from django.contrib.auth.decorators import login_required

from .views import AppLikesCreateView, AppLikesUpdateView, AppLikesDeleteView


urlpatterns = [
    path("create/", login_required(AppLikesCreateView.as_view()), name="create"),
    path("<int:pk>/", login_required(AppLikesUpdateView.as_view()), name="update"),
    path("<int:pk>/delete/", login_required(AppLikesDeleteView.as_view()), name="delete"),
]
