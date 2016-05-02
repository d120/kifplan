from django.views.generic import TemplateView
from django.shortcuts import render,redirect

class Index(TemplateView):
    template_name = 'frontend/index.html'

def beamer_multi(request, *args, **kwargs):
    return redirect("http://caroline.d120.de/beamer/")
