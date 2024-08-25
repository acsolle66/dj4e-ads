from django.template.response import TemplateResponse
from django.http.request import HttpRequest
from django.http.response import HttpResponseRedirect
from .forms import LoginForm
from django.urls import reverse
from django.contrib.auth import authenticate, login


# Create your views here.
def home_view(request):
    return TemplateResponse(request, "home/home.html", {})


def login_view(request: HttpRequest):
    if request.user.is_authenticated:
        return HttpResponseRedirect(reverse("ads:ads_list"))

    if request.method == "POST":
        form = LoginForm(request.POST)
        username = request.POST["username"]
        password = request.POST["password"]
        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            return HttpResponseRedirect(reverse("ads:ads_list"))
        form_error_msg = True
    else:
        form_error_msg = False
        form = LoginForm()

    return TemplateResponse(
        request,
        "registration/login.html",
        {"form": form, "form_error_msg": form_error_msg},
    )
