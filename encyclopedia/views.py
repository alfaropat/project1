from django.shortcuts import render

from . import util
from django import forms
from django.http import HttpResponse


def index(request):
    return render(request, "encyclopedia/index.html", {
        "entries": util.list_entries()
    })

def error(request, name):
    return render(request, "encyclopedia/error.html", {
        "entry": name
    })

def add(request):
    if request.method == "POST":

        form = NewEntryForm(request.POST)

        if form.is_valid():
            entry_name = form.cleaned_data["entry_name"]
            entry_info = form.cleaned_data["entry_info"]

            util.save_entry(entry_name,entry_info)

            return render(request, "encyclopedia/entry.html", {
                "entry_name": entry_name,
                "entry_info": entry_info
            })

    return render(request, "encyclopedia/add.html", {
        "form": NewEntryForm(),
    })

class NewEntryForm():
    entry_name = forms.CharField(label="Entry Name")
    entry_info = forms.CharField(label="Entry Info")

def entry(request, name):
    if util.get_entry(name) != None:
        return render(request, "encyclopedia/entry.html", {
        "entry_name": name,
        "entry_info": util.get_entry(name)
    })
    error(request, name)

def random(request):
    entry_chosen = random.choice(util.list_entries())

    return render(request, "encyclopedia/entry.html", {
        "entry_name": entry_chosen,
        "entry_info": util.get_entry(entry_chosen)
    })

def search(request, name):

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

def entry(request, name):
    full_entry = util.get_entry(name)

    return render(request, "encyclopedia/entry.html", {
        "entry_name": name,
        "entry_info": full_entry[len(name)+2:len(full_entry)-1]
    })


