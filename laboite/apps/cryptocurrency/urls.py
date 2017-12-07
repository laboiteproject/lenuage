from django.conf.urls import url
from django.contrib.auth.decorators import login_required

from .views import AppCryptocurrencyCreateView, AppCryptocurrencyUpdateView, AppCryptocurrencyDeleteView


urlpatterns = [
    url(r"^create/$", login_required(AppCryptocurrencyCreateView.as_view()), name="create"),
    url(r"^(?P<pk>\d+)/$", login_required(AppCryptocurrencyUpdateView.as_view()), name="update"),
    url(r"^(?P<pk>\d+)/delete/$", login_required(AppCryptocurrencyDeleteView.as_view()), name="delete"),
]
