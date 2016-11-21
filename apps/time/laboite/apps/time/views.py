from django.shortcuts import render
from django.views.generic.edit import UpdateView

from .models import AppTime

class AppTimeUpdateView(UpdateView):
    model = AppTime
    fields = ['tz']

    success_url = '../../'

    def get_context_data(self, **kwargs):
        context = super(AppTimeUpdateView, self).get_context_data(**kwargs)
        verbose_name = self.object._meta.verbose_name.title()
        context['verbose_name'] = verbose_name
        context['boite_id'] = self.kwargs.get('boite_pk')

        return context