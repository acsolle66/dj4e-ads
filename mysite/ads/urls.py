from django.urls import path
from . import views

app_name = "ads"

urlpatterns = [
    path("ads/", views.ads_list_view, name="ads_list"),
    path("ad/create/", views.ads_create_view, name="ads_create"),
    path("ad/<int:pk>/", views.ads_detail_view, name="ads_detail"),
    path("ad/<int:pk>/update/", views.ad_update, name="ad_update"),
    path("ad/<int:pk>/delete/", views.ad_delete, name="ad_delete"),
    path("ad/picture/<int:pk>/", views.stream_file, name="ad_picture"),
    path("ad/comment/<int:pk>/delete/", views.comment_delete, name="comment_delete"),
]
