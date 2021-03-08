from django.urls import path

from . import views

urlpatterns = [
    path("", views.index, name="index"),
    path("error", views.error, name="error"),
    path("add", views.add, name="add"),
    path("<str:name>", views.entry, name="entry"),
    path("entry/<str:name>", views.random, name="random"),
    path("search/<str:name>", views.search, name="search")
]
