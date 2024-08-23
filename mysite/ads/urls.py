from django.urls import path
from . import views

app_name = "ads"

urlpatterns = [
    path("", views.ads_list_view, name="ads_list_view"),
]
