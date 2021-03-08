from django.shortcuts import render

from . import util


def index(request):
    return render(request, "encyclopedia/index.html", {
        "entries": util.list_entries()
    })

def search(request,name):
    if util.get_entry(name) != None:
        return render(request, "encyclopedia/entry.html", {
            "entry_name": name,
            "entry_info": util.get_entry(name)
        })

    return render(request, "encyclopedia/search.html", {
        "substring": name
    })
