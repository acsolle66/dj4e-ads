from ast import arg
from django.db.models.manager import BaseManager
from django.http import HttpResponse, HttpRequest, HttpResponseRedirect
from django.template.response import TemplateResponse
from django.contrib.auth.decorators import login_required
from django.urls import reverse
from ads.models import Ad, Comment
from ads.forms import AdForm, CommentForm
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
    ad: Ad = get_object_or_404(Ad, pk=pk)
    comments: BaseManager[Comment] = Comment.objects.filter(ad=ad).order_by(
        "-created_at"
    )
    comment_create_form = CommentForm()

    return TemplateResponse(
        request,
        "ads/ad_detail.html",
        {"ad": ad, "comments": comments, "comment_create_form": comment_create_form},
    )


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


# FOR IMAGE UPLOAD
def stream_file(request, pk):
    instance: Ad = get_object_or_404(Ad, id=pk)
    img: bytes | None = instance.picture
    response = HttpResponse()
    response["Content-Type"] = instance.img_content_type
    response["Content-Length"] = len(img)
    response.write(img)
    return response


# INFO: COMMENTS
def comment_delete(request: HttpRequest, pk) -> HttpResponse:
    comment: Comment = get_object_or_404(Comment, id=pk)
    ad_id = comment.ad.pk
    redirect_url: str = reverse("ads:ads_detail", args=[ad_id])

    # Check if user is logged in
    if not request.user.is_authenticated:
        return HttpResponseRedirect(redirect_url)

    # Check if user owns the model object
    if comment.owner != request.user:
        return HttpResponseRedirect(redirect_url)

    else:
        if request.method == "POST":
            comment.delete()
            return HttpResponseRedirect(redirect_url)
        return TemplateResponse(
            request, "comments/comment_delete.html", {"comment": comment}
        )


def comment_create(request: HttpRequest, pk) -> HttpResponse:
    if request.method == "POST":
        comment_form = CommentForm(request.POST)
        if comment_form.is_valid():
            comment_text = comment_form.cleaned_data["comment"]
            comment_ad = get_object_or_404(Ad, id=pk)
            comment_owner = request.user

            comment: Comment = Comment(
                text=comment_text, owner=comment_owner, ad=comment_ad
            )
            comment.save()
        return HttpResponseRedirect(reverse("ads:ads_detail", args=[pk]))
