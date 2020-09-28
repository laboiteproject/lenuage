from django.urls import include, path
from django.conf import settings
from django.conf.urls.static import static
from django.views.generic import TemplateView

from django.contrib import admin

from .views import home_view, help_view


urlpatterns = [
    path("", home_view, name="home"),
    path("admin/", admin.site.urls),
    path("account/", include("account.urls")),
    path("account/social/accounts/", TemplateView.as_view(template_name="account/social.html"), name="account_social_accounts"),
    path("account/social/", include("social.apps.django_app.urls", namespace="social")),
    path("boites/", include('boites.urls', namespace="boites")),
    path("help/", help_view, name="help"),
]

urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
