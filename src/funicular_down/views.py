from django.views.generic import TemplateView

from .models import Server, get_status_from_server


class BaseTemplateView(TemplateView):
    template_name = "funicular_down/base_app.html"


class GetStatusTemplateView(TemplateView):
    template_name = "funicular_down/control.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["status"] = {}
        for server in Server.objects.filter(active=True):
            context["status"][server] = get_status_from_server(server)
        return context
