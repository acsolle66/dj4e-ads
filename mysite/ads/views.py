from django.http import HttpResponse, HttpRequest, HttpResponseRedirect
from django.template.response import TemplateResponse
from django.contrib.auth.decorators import login_required
from django.urls import reverse
from ads.models import Ad
from ads.forms import AdForm
from django.shortcuts import get_object_or_404


# Create your views here.
def ads_list_view(request: HttpRequest) -> HttpResponse:
    ads = Ad.objects.all()
    return TemplateResponse(request, "ads/ads_list.html", {"ads": ads})


@login_required()
def ads_create_view(request: HttpRequest) -> HttpResponse:
    if request.method == "POST":
        form = AdForm(request.POST, request.FILES or None)
        if form.is_valid():
            form: Ad = form.save(commit=False)
            form.owner = request.user
            form.save()
            return HttpResponseRedirect(reverse("ads:ads_list"))
    else:
        form = AdForm()
    return TemplateResponse(request, "ads/ad_create.html", {"form": form})


def ads_detail_view(request: HttpRequest, pk: int) -> HttpResponse:
    object = get_object_or_404(Ad, pk=pk)

    return TemplateResponse(request, "ads/ad_detail.html", {"ad": object})


def ad_update(request: HttpRequest, pk: int):
    # Check if user is logged in
    if not request.user.is_authenticated:
        return HttpResponseRedirect(reverse("home:login"))

    # Check if user owns the model object
    object = get_object_or_404(Ad, pk=pk)
    if object.owner != request.user:
        return HttpResponseRedirect(reverse("ads:ads_list"))
    else:
        if request.method == "POST":
            form = AdForm(request.POST, request.FILES or None, instance=object)
            if form.is_valid():
                form.save()
                return HttpResponseRedirect(reverse("ads:ads_list"))
        else:
            form = AdForm(instance=object)
        return TemplateResponse(request, "ads/ad_create.html", {"form": form})


def ad_delete(request: HttpRequest, pk: int) -> HttpResponse:
    # Check if user is logged in
    if not request.user.is_authenticated:
        return HttpResponseRedirect(reverse("home:login"))

    # Check if user owns the model object
    object = get_object_or_404(Ad, pk=pk)
    if object.owner != request.user:
        return HttpResponseRedirect(reverse("ads:ads_list"))
    else:
        if request.method == "POST":
            object.delete()
            return HttpResponseRedirect(reverse("ads:ads_list"))
        return TemplateResponse(request, "ads/ad_delete.html", {"ad": object})


def stream_file(request, pk):
    instance: Ad = get_object_or_404(Ad, id=pk)
    img: bytes | None = instance.picture
    response = HttpResponse()
    response["Content-Type"] = instance.img_content_type
    response["Content-Length"] = len(img)
    response.write(img)
    return response
