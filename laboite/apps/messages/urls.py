from django.urls import path
from django.contrib.auth.decorators import login_required

from .views import AppMessagesUpdateView, AppMessagesCreateView, AppMessagesDeleteView

app_name = "laboite"

urlpatterns = [
    path("create/", login_required(AppMessagesCreateView.as_view()), name="create"),
    path("<int:pk>/", login_required(AppMessagesUpdateView.as_view()), name="update"),
    path("<int:pk>/delete/", login_required(AppMessagesDeleteView.as_view()), name="delete"),
]
