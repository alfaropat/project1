from django.shortcuts import render

from . import util
from django import forms


def index(request):
    return render(request, "encyclopedia/index.html", {
        "entries": util.list_entries()
    })

def search(request):

    if request.method == "POST":
        form = NewSearchForm(request.POST)

        if form.is_valid():
            search = form.cleaned_data["search"]

            if util.get_entry(search) != None:
                return render(request, "encyclopedia/entry.html", {
                    "entry_name": search,
                    "entry_info": util.get_entry(search)
                })

            else:
                search_list = any(search in entry for entry in util.list_entries())
                
                return render(request, "encyclopedia/search.html", {
                    "search_substring": search,
                    "search_list": search_list
                })
                    
        return render(request, "encyclopedia/search.html", {
            "form": NewSearchForm()
        })

class NewSearchForm(forms.Form):
    search = forms.CharField(label="New Search")

def entry(request):

    if util.get_entry(request.GET) != None:
        return render(request, "encyclopedia/entry.html", {
        "entry_name": request.GET,
        "entry_info": util.get_entry(request.GET)
    })
   # error(request, name)

