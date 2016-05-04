from django.views.generic import TemplateView
from django.shortcuts import render,redirect
from neuigkeiten.models import Beitrag

class Index(TemplateView):
    template_name = 'frontend/index.html'
    
    def get_context_data(self, **kwargs):
        context = super(Index, self).get_context_data(**kwargs)
        context['news'] = Beitrag.objects.all().order_by("-published_date")[0:5]
        return context

def beamer_multi(request, *args, **kwargs):
    return redirect("http://caroline.d120.de/beamer/")
