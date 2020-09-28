from django.urls import path
from django.contrib.auth.decorators import login_required

from .views import AppCryptocurrencyCreateView, AppCryptocurrencyUpdateView, AppCryptocurrencyDeleteView

app_name = "laboite"

urlpatterns = [
    path("create/", login_required(AppCryptocurrencyCreateView.as_view()), name="create"),
    path("<int:pk>/", login_required(AppCryptocurrencyUpdateView.as_view()), name="update"),
    path("<int:pk>/delete/", login_required(AppCryptocurrencyDeleteView.as_view()), name="delete"),
]
