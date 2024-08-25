from django.urls import path
from . import views
from ads.views import ads_list_view

app_name = "home"


urlpatterns = [
    path("", ads_list_view, name="home"),
    path("login/", views.login_view, name="login"),
]
