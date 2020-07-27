from django.urls import path
from django.contrib.auth.decorators import login_required

from .views import AppMetroUpdateView, AppMetroCreateView, AppMetroDeleteView

urlpatterns = [
    path("create/", login_required(AppMetroCreateView.as_view()), name="create"),
    path("<int:pk>/", login_required(AppMetroUpdateView.as_view()), name="update"),
    path("<int:pk>/delete/", login_required(AppMetroDeleteView.as_view()), name="delete"),
]
