from django.shortcuts import render

from . import util


def index(request):
    return render(request, "encyclopedia/index.html", {
        "entries": util.list_entries()
    })

def edit(request,name):
    if request.method == "POST":
        
        form = NewEntryForm(request.POST)

        if form.is_valid():
            entry_info = form.cleaned_data["entry_info"]
            util.save_entry(name,entry_info)

            return render(request, "encyclopedia/entry.html", {
                "name": name
            })

        else:

            return render(request, "encyclopedia/add.html", {
                "form": form
            })

    return render(request, "encyclopedia/html", {
        "form": NewEntryForm()
    })
