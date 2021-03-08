from django.shortcuts import render

from . import util


def index(request):
    return render(request, "encyclopedia/index.html", {
        "entries": util.list_entries()
    })

def random(request):
    entry_chosen = random.choice(util.list_entries())

    return render(request, "encyclopedia/entry.html", {
        "entry_name": entry_chosen,
        "entry_info": util.get_entry(entry_chosen)
    })
