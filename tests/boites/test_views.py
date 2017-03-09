import pytest

from django.contrib.auth.models import User
from django.http import Http404
from django.urls import reverse

from boites.models import Boite
from boites.views import BoiteUpdateView, BoiteDeleteView


@pytest.mark.django_db
def test_boite_ownership_views(rf):
    user1 = User.objects.create_user('user1')
    user2 = User.objects.create_user('user2')
    boite = Boite(name='boite', user=user1)
    boite.save()
    kw = {'pk': boite.pk}

    # Test boite UpdateView
    url = reverse('boites:update', kwargs=kw)
    view = BoiteUpdateView.as_view()
    request = rf.get(url)
    request.user = user1
    response = view(request, **kw)
    assert response.status_code == 200
    request.user = user2
    with pytest.raises(Http404):
        view(request, **kw)

    # Test boite DeleteView
    url = reverse('boites:delete', kwargs=kw)
    view = BoiteDeleteView.as_view()
    request = rf.get(url)
    request.user = user1
    response = view(request, **kw)
    assert response.status_code == 200
    request.user = user2
    with pytest.raises(Http404):
        view(request, **kw)
