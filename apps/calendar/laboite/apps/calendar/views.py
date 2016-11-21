from django.views.generic.edit import UpdateView

from .models import AppCalendar


class AppCalendarUpdateView(UpdateView):
    model = AppCalendar
    fields = ['ics_url']

    success_url = '../../'

    def get_context_data(self, **kwargs):
        context = super(AppCalendarUpdateView, self).get_context_data(**kwargs)
        verbose_name = self.object._meta.verbose_name.title()
        context['verbose_name'] = verbose_name
        context['boite_id'] = self.kwargs.get('boite_pk')

        return context
