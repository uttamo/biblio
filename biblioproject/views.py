import datetime as dt

from django.views.generic import TemplateView


class HomepageView(TemplateView):
    template_name = 'home.html'

    def get_context_data(self, **kwargs):
        context_data = super().get_context_data(**kwargs)
        context_data['current_time'] = dt.datetime.now()
        return context_data
