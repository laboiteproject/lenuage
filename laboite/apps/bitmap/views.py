# coding: utf-8
from __future__ import unicode_literals
from .models import AppBitmap, Bitmap
from boites.views import AppCreateView, AppUpdateView, AppDeleteView


class AppBitmapCreateView(AppCreateView):
    model = AppBitmap
    fields = ['width', 'height']


class AppBitmapUpdateView(AppUpdateView):
    model = AppBitmap
    template_name = 'bitmap_form.html'
    fields = ['width', 'height', 'color', 'enabled']

    def get_context_data(self, **kwargs):
        context = super(AppBitmapUpdateView, self).get_context_data(**kwargs)

        bitmaps = Bitmap.objects.filter(app_id=self.object.id)
        context['bitmaps'] = bitmaps

        return context

    def form_valid(self, form):
        #delete all previous bitmaps
        bitmaps = Bitmap.objects.filter(app_id=self.object.id)
        bitmaps.delete()
        
        # save bitmap(s) from form
        for key in self.request.POST:
            # if this is a bitmap
            if key.startswith("id_bitmap"):
                bitmap = Bitmap(app_id=self.kwargs.get('pk'), bitmap=self.request.POST.get(key))
                bitmap.save()
        return super(AppBitmapUpdateView, self).form_valid(form)

class AppBitmapDeleteView(AppDeleteView):
    model = AppBitmap
