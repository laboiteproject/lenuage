from django.urls import path
from django.contrib.auth.decorators import login_required

from .views import AppCalendarUpdateView, AppCalendarCreateView, AppCalendarDeleteView

app_name = "laboite"

urlpatterns = [
    path("create/", login_required(AppCalendarCreateView.as_view()), name="create"),
    path("<int:pk>/", login_required(AppCalendarUpdateView.as_view()), name="update"),
    path("<int:pk>/delete/", login_required(AppCalendarDeleteView.as_view()), name="delete"),
]
