from django.views.generic.edit import UpdateView

from .models import AppMessages

class AppMessagesUpdateView(UpdateView):
    model = AppMessages
    fields = ['message']

    success_url = '../../'

    def get_context_data(self, **kwargs):
        context = super(AppMessagesUpdateView, self).get_context_data(**kwargs)
        verbose_name = self.object._meta.verbose_name.title()
        context['verbose_name'] = verbose_name
        context['boite_id'] = self.kwargs.get('boite_pk')

        return context
