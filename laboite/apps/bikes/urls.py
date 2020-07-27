from django.urls import path
from django.contrib.auth.decorators import login_required

from .views import StationAutoComplete, AppBikesCreateView, AppBikesUpdateView, AppBikesDeleteView

app_name = "laboite"

urlpatterns = [
    path("station-autocomplete/",
        login_required(StationAutoComplete.as_view()),
        name='station-autocomplete'),
    path("create/", login_required(AppBikesCreateView.as_view()), name="create"),
    path("<int:pk>/", login_required(AppBikesUpdateView.as_view()), name="update"),
    path("<int:pk>/delete/", login_required(AppBikesDeleteView.as_view()), name="delete"),
]
