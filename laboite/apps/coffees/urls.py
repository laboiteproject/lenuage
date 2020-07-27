from django.urls import path
from django.contrib.auth.decorators import login_required

from .views import AppCoffeesCreateView, AppCoffeesUpdateView, AppCoffeesDeleteView

app_name = "laboite"

urlpatterns = [
    path("create/", login_required(AppCoffeesCreateView.as_view()), name="create"),
    path("<int:pk>/", login_required(AppCoffeesUpdateView.as_view()), name="update"),
    path("<int:pk>/delete/", login_required(AppCoffeesDeleteView.as_view()), name="delete"),
]
