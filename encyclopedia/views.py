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
    
    entries_substring = any(name in entry for entry in util.list_entries())

    return render(request, "encyclopedia/search.html", {
        "substring": name,
        "entries": entries_substring
    })
