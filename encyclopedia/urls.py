from django.urls import path

from . import views
from django.conf.urls import url
from django.views.generic import RedirectView

app_name = "encyclopedia"
urlpatterns = [
    url(r'^$', views.redirect_index),
    path("wiki", views.index, name="index"),
    path("search", views.search, name="search"),
    path("rand", views.redirect_random, name="rand"),
    path('wiki/<str:name>', views.entry, name="entry")
]
