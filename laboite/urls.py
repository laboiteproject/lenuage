from django.conf import settings
from django.conf.urls import include, url
from django.conf.urls.static import static
from django.views.generic import TemplateView

from django.contrib import admin

from .views import home_view, help_view


urlpatterns = [
    url(r"^$", home_view, name="home"),
    url(r"^admin/", include(admin.site.urls)),
    url(r"^account/", include("account.urls")),
    url(r"^account/social/accounts/$", TemplateView.as_view(template_name="account/social.html"), name="account_social_accounts"),
    url(r"^account/social/", include("social.apps.django_app.urls", namespace="social")),
    url(r'^boites/', include('boites.urls', namespace="boites")),
    url(r'^help/', help_view, name="help"),
]

urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
