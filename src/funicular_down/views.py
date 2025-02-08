from django.views.generic import TemplateView

from .models import get_status_from_server


class GetStatusTemplateView(TemplateView):
    template_name = "funicular_down/control.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["status"] = get_status_from_server()
        return context
