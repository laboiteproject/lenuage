from django.conf.urls import include, url
from django.contrib.auth.decorators import login_required

from .views import AppMessagesUpdateView, AppMessagesCreateView, AppMessagesDeleteView

urlpatterns = [
    url(r"^create/$", login_required(AppMessagesCreateView.as_view()), name="create"),
    url(r"^(?P<pk>\d+)/$", login_required(AppMessagesUpdateView.as_view()), name="update"),
    url(r"^(?P<pk>\d+)/delete/$", login_required(AppMessagesDeleteView.as_view()), name="delete"),
]
