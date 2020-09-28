from django.urls import path
from django.contrib.auth.decorators import login_required

from .views import AppTrafficCreateView, AppTrafficUpdateView, AppTrafficDeleteView

app_name = "laboite"

urlpatterns = [
    path("create/", login_required(AppTrafficCreateView.as_view()), name="create"),
    path("<int:pk>/", login_required(AppTrafficUpdateView.as_view()), name="update"),
    path("<int:pk>/delete/", login_required(AppTrafficDeleteView.as_view()), name="delete"),
]
