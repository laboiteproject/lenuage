# coding: utf-8
from __future__ import unicode_literals
from .models import AppCustom, Bitmap
from boites.views import AppCreateView, AppUpdateView, AppDeleteView


class AppCustomCreateView(AppCreateView):
    model = AppCustom
    template_name = 'custom_form.html'
    fields = ['width', 'height']


class AppCustomUpdateView(AppUpdateView):
    model = AppCustom
    template_name = 'custom_form.html'
    fields = ['width', 'height', 'enabled']

    def get_context_data(self, **kwargs):
        context = super(AppCustomUpdateView, self).get_context_data(**kwargs)

        bitmaps = Bitmap.objects.filter(app_id=self.object.id)
        context['bitmaps'] = bitmaps

        return context

    def form_valid(self, form):
        for key in self.request.POST:
            if key.startswith("id_bitmap"):
                id = int(key[9:])
                bitmap = Bitmap(id=id, app_id=self.kwargs.get('pk'), bitmap=self.request.POST.get(key))
                bitmap.save()
        return super(AppCustomUpdateView, self).form_valid(form)

class AppCustomDeleteView(AppDeleteView):
    model = AppCustom
