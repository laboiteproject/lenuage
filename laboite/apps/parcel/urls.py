from django.urls import path
from django.contrib.auth.decorators import login_required

from .views import AppParcelUpdateView, AppParcelCreateView, AppParcelDeleteView

app_name = "laboite"

urlpatterns = [
    path("create/", login_required(AppParcelCreateView.as_view()), name="create"),
    path("<int:pk>/", login_required(AppParcelUpdateView.as_view()), name="update"),
    path("<int:pk>/delete/", login_required(AppParcelDeleteView.as_view()), name="delete"),
]
