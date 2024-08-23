from django.http import HttpResponse
from django.template.response import TemplateResponse


# Create your views here.
def ads_list_view(request) -> HttpResponse:
    return TemplateResponse(request, "ads/ads_list_view.html", {})
