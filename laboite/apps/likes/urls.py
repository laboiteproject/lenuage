from django.conf.urls import url
from django.contrib.auth.decorators import login_required

from .views import AppLikesCreateView, AppLikesUpdateView, AppLikesDeleteView


urlpatterns = [
    url(r"^create/$", login_required(AppLikesCreateView.as_view()), name="create"),
    url(r"^(?P<pk>\d+)/$", login_required(AppLikesUpdateView.as_view()), name="update"),
    url(r"^(?P<pk>\d+)/delete/$", login_required(AppLikesDeleteView.as_view()), name="delete"),
]
