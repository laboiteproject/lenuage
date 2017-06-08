from django.conf.urls import url
from django.contrib.auth.decorators import login_required

from .views import AppCoffeesCreateView, AppCoffeesUpdateView, AppCoffeesDeleteView


urlpatterns = [
    url(r"^create/$", login_required(AppCoffeesCreateView.as_view()), name="create"),
    url(r"^(?P<pk>\d+)/$", login_required(AppCoffeesUpdateView.as_view()), name="update"),
    url(r"^(?P<pk>\d+)/delete/$", login_required(AppCoffeesDeleteView.as_view()), name="delete"),
]
