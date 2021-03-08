from django.shortcuts import render

from . import util
from django.http import HttpResponse


def index(request):
    return render(request, "encyclopedia/index.html", {
        "entries": util.list_entries()
    })

def entry(request, name):
    return HttpResponse(render(request, "encyclopedia/entry.html", {
        "entry": util.get_entry(name)
    })
