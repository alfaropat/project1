from django.urls import path

from . import views

app_name = "encyclopedia"
urlpatterns = [
    path("", views.index, name="index"),
    path("error", views.error, name="error"),
    path("add", views.add, name="add"),
    path('<str:name>', views.entry, name="entry"),
    path("random", views.random, name="random"),
    path("search", views.search, name="search")
]
