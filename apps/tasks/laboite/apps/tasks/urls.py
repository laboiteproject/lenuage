from django.conf.urls import url
from django.contrib.auth.decorators import login_required

from .views import AppTasksUpdateView, AppTasksCreateView, AppTasksDeleteView, get_projects_view

urlpatterns = [
    url(r"^create/$", login_required(AppTasksCreateView.as_view()), name="create"),
    url(r"^(?P<pk>\d+)/$", login_required(AppTasksUpdateView.as_view()), name="update"),
    url(r"^(?P<pk>\d+)/delete/$", login_required(AppTasksDeleteView.as_view()), name="delete"),
    url(r"^projects$", login_required(get_projects_view), name="get_projects"),
]
