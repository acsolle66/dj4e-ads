from django.shortcuts import render
from django.template.response import TemplateResponse


# Create your views here.
def home_view(request):
    return TemplateResponse(request, "home/home.html", {})
